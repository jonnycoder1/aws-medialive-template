import boto3
import logging
logger = logging.getLogger(__name__)

class AWSLiveStream:
    def __init__(self):
        self.youtube_stream_url = "rtmp://a.rtmp.youtube.com/live2"
        self.facebook_stream_url = "rtmps://live-api-s.facebook.com:443/rtmp/"

        # Add your inputs here
        self.youtube_stream_key = "ADD YOUTUBE STREAM KEY HERE"
        self.facebook_stream_key = "ADD FACEBOOK STREAM KEY HERE"
        self.aws_access_key_id = "ADD KEY HERE"
        self.aws_secret_access_key = "ADD SECRET HERE"
        self.aws_region = "ADD REGION HERE"

        self.client = boto3.client("medialive",
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key,
                                   region_name=self.aws_region)

    def create_livestream(self, title: str):
        security_group_id = self._create_input_security_group()
        input_id = self._create_input(title=title, security_group_id=security_group_id)
        channel_id, channel_arn = self._create_channel(input_id=input_id)
        rtmp_url = self.client.describe_input(InputId=input_id)["Destinations"][0]["Url"]
        logger.info("Created livestream at %s", rtmp_url)

    def _create_input_security_group(self) -> str:
        whitelist_rules = [{"Cidr": "0.0.0.0/0"}]
        sg_resp = self.client.create_input_security_group(WhitelistRules=whitelist_rules)
        return sg_resp["SecurityGroup"]["Id"]

    def _create_input(self, title: str, security_group_id: str) -> str:
        input_resp = self.client.create_input(InputSecurityGroups=[security_group_id],
                                              Type="RTMP_PUSH",
                                              Destinations=[{'StreamName': "input1/%s" % title}],
                                              Name="%s_input" % title)
        return input_resp["Input"]["Id"]

    def _create_channel(self, title: str, input_id: str):
        response = self._get_client().create_channel(
            ChannelClass="SINGLE_PIPELINE",
            Destinations=[
                {
                    "Id": "YouTube-Destination",
                    "Settings": [
                        {
                            "Url": self.youtube_stream_url,
                            "StreamName": self.youtube_stream_key,
                        }
                    ],
                    "MediaPackageSettings": []
                },
                {
                    "Id": "Facebook-Destination",
                    "Settings": [
                        {
                            "Url": self.facebook_stream_url,
                            "StreamName": self.facebook_stream_key,
                        }
                    ],
                    "MediaPackageSettings": []
                }
            ],
            InputAttachments=[{
                "InputId": input_id
            }],
            EncoderSettings={
                "TimecodeConfig": {
                    "Source": "SYSTEMCLOCK"
                },
                "OutputGroups": [
                    {
                        "OutputGroupSettings": {
                            "RtmpGroupSettings": {
                                "AuthenticationScheme": "COMMON",
                                "CacheLength": 30,
                                "RestartDelay": 15,
                                "CacheFullBehavior": "DISCONNECT_IMMEDIATELY",
                                "CaptionData": "ALL",
                                "InputLossAction": "EMIT_OUTPUT",
                                "AdMarkers": []
                            }
                        },
                        "Name": "YouTube Live",
                        "Outputs": [
                            {
                                "OutputSettings": {
                                    "RtmpOutputSettings": {
                                        "Destination": {
                                            "DestinationRefId": "YouTube-Destination"
                                        },
                                        "ConnectionRetryInterval": 2,
                                        "NumRetries": 10,
                                        "CertificateMode": "VERIFY_AUTHENTICITY"
                                    }
                                },
                                "OutputName": "YouTube-Destination",
                                "VideoDescriptionName": "video_1080p30",
                                "AudioDescriptionNames": [
                                    "audio_youtube"
                                ],
                                "CaptionDescriptionNames": []
                            }
                        ]
                    },
                    {
                        "OutputGroupSettings": {
                            "RtmpGroupSettings": {
                                "AuthenticationScheme": "COMMON",
                                "CacheLength": 30,
                                "RestartDelay": 15,
                                "CacheFullBehavior": "DISCONNECT_IMMEDIATELY",
                                "CaptionData": "ALL",
                                "InputLossAction": "EMIT_OUTPUT",
                                "AdMarkers": []
                            }
                        },
                        "Name": "Facebook",
                        "Outputs": [
                            {
                                "OutputSettings": {
                                    "RtmpOutputSettings": {
                                        "Destination": {
                                            "DestinationRefId": "Facebook-Destination"
                                        },
                                        "ConnectionRetryInterval": 2,
                                        "NumRetries": 10,
                                        "CertificateMode": "VERIFY_AUTHENTICITY"
                                    }
                                },
                                "OutputName": "Facebook-Destination",
                                "VideoDescriptionName": "video_720p30",
                                "AudioDescriptionNames": [
                                    "audio_facebook"
                                ],
                                "CaptionDescriptionNames": []
                            }
                        ]
                    }
                ],
                "GlobalConfiguration": {
                    "SupportLowFramerateInputs": "DISABLED",
                    "OutputTimingSource": "SYSTEM_CLOCK",
                    "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
                },
                "CaptionDescriptions": [],
                "VideoDescriptions": [
                    {
                        "CodecSettings": {
                            "H264Settings": {
                                "Syntax": "DEFAULT",
                                "FramerateNumerator": 30,
                                "Profile": "HIGH",
                                "GopSize": 2,
                                "AfdSignaling": "NONE",
                                "FramerateControl": "SPECIFIED",
                                "ColorMetadata": "INSERT",
                                "FlickerAq": "ENABLED",
                                "LookAheadRateControl": "HIGH",
                                "FramerateDenominator": 1,
                                "Bitrate": 6000000,
                                "TimecodeInsertion": "PIC_TIMING_SEI",
                                "NumRefFrames": 3,
                                "EntropyEncoding": "CABAC",
                                "GopSizeUnits": "SECONDS",
                                "Level": "H264_LEVEL_AUTO",
                                "GopBReference": "ENABLED",
                                "AdaptiveQuantization": "HIGH",
                                "GopNumBFrames": 3,
                                "ScanType": "PROGRESSIVE",
                                "ParControl": "INITIALIZE_FROM_SOURCE",
                                "Slices": 1,
                                "SpatialAq": "ENABLED",
                                "TemporalAq": "ENABLED",
                                "RateControlMode": "CBR",
                                "SceneChangeDetect": "ENABLED",
                                "GopClosedCadence": 1
                            }
                        },
                        "Name": "video_1080p30",
                        "Sharpness": 50,
                        "Height": 1080,
                        "Width": 1920,
                        "ScalingBehavior": "DEFAULT",
                        "RespondToAfd": "NONE"
                    },
                    {
                        "CodecSettings": {
                            "H264Settings": {
                                "AfdSignaling": "NONE",
                                "ColorMetadata": "INSERT",
                                "AdaptiveQuantization": "HIGH",
                                "Bitrate": 4000000,
                                "EntropyEncoding": "CABAC",
                                "FlickerAq": "ENABLED",
                                "ForceFieldPictures": "DISABLED",
                                "FramerateControl": "SPECIFIED",
                                "FramerateNumerator": 30000,
                                "FramerateDenominator": 1000,
                                "GopBReference": "ENABLED",
                                "GopClosedCadence": 1,
                                "GopNumBFrames": 3,
                                "GopSize": 2,
                                "GopSizeUnits": "SECONDS",
                                "SubgopLength": "FIXED",
                                "ScanType": "PROGRESSIVE",
                                "Level": "H264_LEVEL_AUTO",
                                "LookAheadRateControl": "HIGH",
                                "NumRefFrames": 3,
                                "ParControl": "SPECIFIED",
                                "ParNumerator": 1,
                                "ParDenominator": 1,
                                "Profile": "HIGH",
                                "RateControlMode": "CBR",
                                "Syntax": "DEFAULT",
                                "SceneChangeDetect": "ENABLED",
                                "Slices": 4,
                                "SpatialAq": "ENABLED",
                                "TemporalAq": "ENABLED",
                                "TimecodeInsertion": "DISABLED"
                            }
                        },
                        "Height": 720,
                        "Name": "video_720p30",
                        "RespondToAfd": "NONE",
                        "Sharpness": 100,
                        "ScalingBehavior": "DEFAULT",
                        "Width": 1280
                    }
                ],
                "AudioDescriptions": [
                    {
                        "AudioTypeControl": "FOLLOW_INPUT",
                        "LanguageCodeControl": "FOLLOW_INPUT",
                        "Name": "audio_youtube",
                        "AudioSelectorName": "audio_youtube"
                    },
                    {
                        "AudioTypeControl": "FOLLOW_INPUT",
                        "LanguageCodeControl": "FOLLOW_INPUT",
                        "Name": "audio_facebook",
                        "AudioSelectorName": "audio_facebook"
                    }
                ]
            },
            Name=title)
        return response


if __name__ == "__main__":
    title = "My Livestream posted to YouTube & Facebook"
    live = AWSLiveStream()
    live.create_livestream(title=title)
