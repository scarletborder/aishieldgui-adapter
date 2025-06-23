import asyncio
from api_client import APIClient


async def main():
    # 使用上下文管理器自动管理会话
    async with APIClient() as client:
        # 示例UUID
        uuid = "test-uuid-123"

        try:
            # 更新状态为"creating"
            status_response = await client.update_status(
                uuid=uuid, status="creating", message="开始创建项目"
            )
            print(f"状态更新响应: {status_response.msg}")

            # 更新进度
            progress_response = await client.update_progress(
                uuid=uuid, progress=50, message="处理中..."
            )
            print(f"进度更新响应: {progress_response.msg}")

            # 提交结果
            result_data = {
                "result": "success",
                "details": {"accuracy": 0.95, "time_taken": "2.5s"},
            }
            result_response = await client.submit_result(
                uuid=uuid, result_data=result_data
            )
            print(f"结果提交响应: {result_response.msg}")

        except Exception as e:
            print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
