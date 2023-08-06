import os
import json
import boto3
import cartopy
from nacis.features import features, Feature


class Preloader:
    def __init__(self, bucket, prefix, rootpath="/tmp"):
        """
        Nacis shapefile Preloader. Stores shapefiles in private s3 bucket for reliable use by cartopy.
        """
        self.s3_bucket = bucket.strip("/")  # no leading/trailing slashes
        self.s3_prefix = prefix.strip("/")  # no leading/trailing slashes
        self.shapefile_path = os.path.join(rootpath, "nacis_preloader_shapefiles")
        # verify that we can write to shapefile_path
        try:
            os.makedirs(self.shapefile_path, exist_ok=True)
        except:
            raise Exception("Can not write to shapefile path")
        # set path for pre existing data:
        cartopy.config["pre_existing_data_dir"] = self.shapefile_path

    def get_known_features(self):
        """
        Get list of know cartopy features
        """
        return features

    def get_archived_features(self):
        """
        Get list of currently archived features
        """
        s3client = boto3.client("s3")
        type_response = s3client.list_objects_v2(
            Bucket=self.s3_bucket, Prefix=self.s3_prefix + "/", Delimiter="/"
        )
        available_features = []
        if "CommonPrefixes" not in type_response.keys():
            raise Exception(
                "shapefile archive not found at s3://{self.s3_bucket}/{self.s3_prefix}"
            )

        for feature_type in type_response["CommonPrefixes"]:
            resolution_response = s3client.list_objects_v2(
                Bucket=self.s3_bucket, Prefix=feature_type["Prefix"], Delimiter="/"
            )
            for feature_resolution in resolution_response["CommonPrefixes"]:
                name_response = s3client.list_objects_v2(
                    Bucket=self.s3_bucket,
                    Prefix=feature_resolution["Prefix"],
                    Delimiter="/",
                )
                available_features += [
                    Feature.get_feature_from_s3prefix(feature["Prefix"])
                    for feature in name_response["CommonPrefixes"]
                ]
        return available_features

    def populate_archive(self, features=features, logger=print):
        """
        Download shapefiles from source and archive to s3 for later preloader use
        shapefile zips are downloaded, unzipped and stored as:
        s3://{s3_bucket}/{s3_prefix}/{resolution}/{type}/{feature}/*
            - features:  list of features to archive
        """
        for feature in features:

            logger(
                f"downloading source to s3://{self.s3_bucket}/{feature.get_s3prefix(self.s3_prefix)}"
            )
            feature.download_to_archive(self.s3_bucket, self.s3_prefix)

    def preload(
        self, feature_name, feature_type=None, feature_resolution=None, logger=print
    ):
        """
        Download shapefiles matching the requested feature and resolution.
            - feature_name (requires) : the name of the feature to load (ie roads, countries, etc)
            - feature_type (optional) : cultural or physical (preloader can usually figure this out)
            - feature_resolution (optional) : 10m, 50m or 110m (will load all it not specified)
        """
        features_to_download = [
            f for f in features if f.name.lower() == feature_name.lower()
        ]
        if isinstance(feature_type, str):
            features_to_download = [
                f
                for f in features_to_download
                if f.type.lower() == feature_type.lower()
            ]
        if isinstance(feature_resolution, str):
            features_to_download = [
                f
                for f in features_to_download
                if f.resolution.lower() == feature_resolution.lower()
            ]
        for feature in features_to_download:
            logger(
                f" NACIS Preloader: loading {feature.name}/{feature.type}/{feature.resolution}"
            )
            feature.download_to_local(
                self.s3_bucket, self.s3_prefix, self.shapefile_path
            )
