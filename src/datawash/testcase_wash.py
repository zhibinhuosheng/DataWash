import argparse

from datawash.config.pipeline_config import PipelineConfig
from datawash.pipeline.pipeline_builder import PipelineBuilder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="测试用例语料清洗")
    parser.add_argument("--input", required=False, help="输入路径")
    parser.add_argument("--output", required=False, help="输出目录")
    args = parser.parse_args()
    args.input = "D:/CODE/DataWash/input"
    args.output = "D:/CODE/DataWash/output"
    config = PipelineConfig(
        input_path=args.input,
        output_dir=args.output,
    )

    pipeline = PipelineBuilder.build_test_case_pipeline(config)
    pipeline.run(config)
    print(f"测试用例清洗完成，输出目录: {args.output}")
