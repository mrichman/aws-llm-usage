#!/usr/bin/env python3
import boto3
import datetime
import argparse
from tabulate import tabulate
from botocore.exceptions import ClientError


def get_bedrock_model_usage(region, days=30, detailed=False):
    """
    Retrieve AWS Bedrock model usage information for the specified time period.

    Args:
        region (str): AWS region to query
        days (int): Number of days to look back
        detailed (bool): Whether to include detailed metrics

    Returns:
        dict: Dictionary containing usage information
    """
    try:
        # Create clients
        bedrock = boto3.client("bedrock", region_name=region)
        cloudwatch = boto3.client("cloudwatch", region_name=region)

        # Get list of available foundation models
        response = bedrock.list_foundation_models()
        models = response.get("modelSummaries", [])

        print(f"Found {len(models)} available foundation models in {region}")

        # Set up time range for CloudWatch metrics
        end_time = datetime.datetime.now(datetime.UTC)
        start_time = end_time - datetime.timedelta(days=days)

        usage_data = []

        # Get usage metrics for each model
        for model in models:
            model_id = model.get("modelId")
            provider = model.get("providerName")

            # Get invocation metrics from CloudWatch
            try:
                metrics = cloudwatch.get_metric_statistics(
                    Namespace="AWS/Bedrock",
                    MetricName="Invocations",
                    Dimensions=[{"Name": "ModelId", "Value": model_id}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=days * 24 * 3600,  # Period in seconds
                    Statistics=["Sum"],
                )

                datapoints = metrics.get("Datapoints", [])
                invocation_count = datapoints[0].get("Sum", 0) if datapoints else 0

                # Only include models that have been used
                if invocation_count > 0 or detailed:
                    model_data = {
                        "Model ID": model_id,
                        "Provider": provider,
                        "Invocations": int(invocation_count),
                    }

                    # Add more details if requested
                    if detailed:
                        model_data["Model Name"] = model.get("modelName", "N/A")
                        model_data["Output Modality"] = model.get(
                            "outputModalities", ["N/A"]
                        )[0]
                        model_data["Input Modality"] = model.get(
                            "inputModalities", ["N/A"]
                        )[0]

                    usage_data.append(model_data)

            except ClientError as e:
                print(f"Error getting metrics for {model_id}: {e}")
                continue

        return usage_data

    except ClientError as e:
        print(f"Error accessing AWS Bedrock: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Analyze AWS Bedrock LLM usage")
    parser.add_argument(
        "--region",
        type=str,
        default="us-east-1",
        help="AWS region to analyze (default: us-east-1)",
    )
    parser.add_argument(
        "--days", type=int, default=30, help="Number of days to analyze (default: 30)"
    )
    parser.add_argument(
        "--detailed", action="store_true", help="Show detailed model information"
    )
    parser.add_argument(
        "--all-regions",
        action="store_true",
        help="Check all AWS regions where Bedrock is available",
    )

    args = parser.parse_args()

    bedrock_regions = [
        "us-east-1",
        "us-west-2",
        "ap-northeast-1",
        "ap-southeast-2",
        "eu-central-1",
    ]

    if args.all_regions:
        all_usage = []
        for region in bedrock_regions:
            print(f"\nChecking region: {region}")
            region_usage = get_bedrock_model_usage(region, args.days, args.detailed)
            for item in region_usage:
                item["Region"] = region
            all_usage.extend(region_usage)

        if all_usage:
            print("\nAWS Bedrock LLM Usage Across All Regions:")
            print(tabulate(all_usage, headers="keys", tablefmt="grid"))
        else:
            print("\nNo Bedrock LLM usage found in any region.")
    else:
        usage = get_bedrock_model_usage(args.region, args.days, args.detailed)

        if usage:
            print(f"\nAWS Bedrock LLM Usage in {args.region} (Last {args.days} days):")
            print(tabulate(usage, headers="keys", tablefmt="grid"))
        else:
            print(f"\nNo Bedrock LLM usage found in {args.region}.")


if __name__ == "__main__":
    main()
