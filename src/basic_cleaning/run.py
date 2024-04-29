#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    local_path = run.use_artifact(args.input_artifact]).file()
    df = pd.read_csv(local_path)

    # Filter results between the min_price and max_price
    logger.info("Filtering resuls between the min_price and the max_price")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
     
    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging artifact")
    run.log_artifact(artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="THis steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type= str,
        help= "name of the source data file to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name of the output data file after cleaning",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="the type for the output_artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="a description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="the min price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="the max price to consider",
        required=True
    )


    args = parser.parse_args()

    go(args)
