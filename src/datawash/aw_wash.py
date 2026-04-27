import argparse

from datawash.config.pipeline_config import PipelineConfig
from datawash.pipeline.pipeline_builder import PipelineBuilder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AW 语料清洗")
    parser.add_argument("--input", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出目录")
    args = parser.parse_args()

    config = PipelineConfig(
        input_path=args.input,
        output_dir=args.output,
    )

    pipeline = PipelineBuilder.build_aw_pipeline(config)
    pipeline.run(config)
    print(f"AW 语料清洗完成，输出目录: {args.output}")
