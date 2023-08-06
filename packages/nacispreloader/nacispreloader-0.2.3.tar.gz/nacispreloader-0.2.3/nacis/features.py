import os
import requests
import zipfile
import boto3
import io


class Feature:
    def __init__(
        self,
        feature_name,
        feature_type,
        feature_resolution,
        feature_source_url="",
        feature_alternate_url="",
    ):
        self.name = feature_name
        self.type = feature_type
        self.resolution = feature_resolution
        self.url1 = feature_source_url  # 1st source (nacis)
        self.url2 = feature_alternate_url  # 2nd source (aws)

    @staticmethod
    def get_feature_from_s3prefix(s3key):
        """
        Create a feature from a s3 archive (based on s3 path)
        """
        tokens = s3key.strip("/").split("/")
        feature_name = tokens[-1]
        feature_resolution = tokens[-2]
        feature_type = tokens[-3]
        return Feature(feature_name, feature_type, feature_resolution)

    def get_s3prefix(self, s3prefix):
        """
        Get s3 prefix for archive files for this feature
        """
        return f'{s3prefix.strip("/")}/{self.type}/{self.resolution}/{self.name}/'

    def get_local_path(self, rootpath, filename):
        """
        Cartopy will seek shapefiles in <rootpath>/shapefiles/natural_earth/<cultural|physical>/<filename>
        """
        return os.path.join(rootpath, "natural_earth", self.type, filename)

    def download_to_archive(self, s3bucket, s3prefix):
        """
        Download the source feature shapefiles and load them into s3 archive
        """
        #
        response = requests.get(self.url1)
        if response.status_code != requests.status_codes.codes.ok:
            response = requests.get(self.url2)
            if response.status_code != requests.status_codes.codes.ok:
                raise Exception("No valid download")
        zip_payload = io.BytesIO(response.content)
        zip_data = zipfile.ZipFile(zip_payload)
        #
        s3client = boto3.client("s3")
        target_s3prefix = f'{self.get_s3prefix(s3prefix)}'
        for zipinfo in zip_data.infolist():
            target_s3key = target_s3prefix + zipinfo.filename
            response = s3client.generate_presigned_post(s3bucket, target_s3key)
            payload = io.BytesIO(zip_data.read(zipinfo.filename))
            post_response = requests.post(
                response["url"],
                data=response["fields"],
                files={"file": (target_s3key, payload)},
            )

    def download_to_local(self, s3bucket, s3prefix, localpath):
        """
        Download a feature from the archive and load locally
        """
        s3client = boto3.client("s3")
        shapefile_s3prefix = self.get_s3prefix(s3prefix)
        response = s3client.list_objects_v2(Bucket=s3bucket, Prefix=shapefile_s3prefix)
        if "Contents" not in response.keys():
            raise Exception(
                "shapefiles not found in s3://{s3bucket}/{shapefile_s3prefix}"
            )

        for s3obj in response["Contents"]:
            downloadpath = self.get_local_path(localpath, s3obj["Key"].split("/")[-1])
            print(f'downloading s3://{s3bucket}/{s3obj["Key"]} to {downloadpath}')
            os.makedirs(os.path.dirname(downloadpath),exist_ok=True)
            s3client.download_file(
                s3bucket,
                s3obj["Key"],
                downloadpath
            )


features = [
    Feature(
        "roads",
        "cultural",
        "10m",
        "https://www.naturalearthdata.com/download/10m/cultural/ne_10m_roads.zip",
        "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_roads.zip",
    ),
    Feature(
        "countries",
        "cultural",
        "10m",
        "https://www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip",
        "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip",
    ),
    Feature(
        "countries",
        "cultural",
        "50m",
        "https://www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip",
        "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip",
    ),
    Feature(
        "countries",
        "cultural",
        "110m",
        "https://www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip",
        "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip",
    ),
    Feature(
        "states_provinces",
        "cultural",
        "10m",
        "https://www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces.zip",
        "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip",
    ),
    Feature(
        "states_provinces",
        "cultural",
        "50m",
        "https://www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_1_states_provinces.zip",
        "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_1_states_provinces.zip",
    ),
    Feature(
        "states_provinces",
        "cultural",
        "110m",
        "https://www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_1_states_provinces.zip",
        "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_1_states_provinces.zip",
    ),
    Feature(
        "coastline",
        "physical",
        "10m",
        "https://www.naturalearthdata.com/download/10m/physical/ne_10m_coastline.zip",
        "https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_coastline.zip",
    ),
    Feature(
        "coastline",
        "physical",
        "50m",
        "https://www.naturalearthdata.com/download/50m/physical/ne_50m_coastline.zip",
        "https://naturalearth.s3.amazonaws.com/50m_physical/ne_50m_coastline.zip",
    ),
    Feature(
        "coastline",
        "physical",
        "110m",
        "https://www.naturalearthdata.com/download/110m/physical/ne_110m_coastline.zip",
        "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_coastline.zip",
    ),
    Feature(
        "rivers_lake_centerlines",
        "physical",
        "10m",
        "https://www.naturalearthdata.com/download/10m/physical/ne_10m_rivers_lake_centerlines.zip",
        "https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_rivers_lake_centerlines.zip",
    ),
    Feature(
        "rivers_lake_centerlines",
        "physical",
        "50m",
        "https://www.naturalearthdata.com/download/50m/physical/ne_50m_rivers_lake_centerlines.zip",
        "https://naturalearth.s3.amazonaws.com/50m_physical/ne_50m_rivers_lake_centerlines.zip",
    ),
    Feature(
        "rivers_lake_centerlines",
        "physical",
        "110m",
        "https://www.naturalearthdata.com/download/110m/physical/ne_110m_rivers_lake_centerlines.zip",
        "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_rivers_lake_centerlines.zip",
    ),
]
