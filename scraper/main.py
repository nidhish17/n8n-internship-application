import asyncio
import httpx
from datetime import date, datetime
from database.db_schema import insert_internships
import os


MAIN_API_URL = os.environ.get("MAIN_API_URL")
WEBSITE_URL = os.environ.get("WEBSITE_URL")

semaphore = asyncio.Semaphore(5)


def to_int(value):
    if value is None or value == "":
        return None
    return int(value)


def to_bool(value):
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes")
    return bool(value)

def parse_internship(itn: dict) -> dict:
    slug = itn["slug"]

    # Convert API values to your model choices
    internship_type = (itn.get("type") or "").lower()

    workmode_mapping = {
        "remote": "online",
        "online": "online",
        "onsite": "onsite",
        "on-site": "onsite",
        "hybrid": "hybrid",
    }

    raw_workmode = (itn.get("workMode") or "").lower()
    workmode = workmode_mapping.get(raw_workmode)

    if internship_type not in ("free", "stipend", "paid"):
        raise ValueError(f"Invalid internship type: {internship_type}")

    if raw_workmode and workmode is None:
        raise ValueError(f"Invalid work mode: {raw_workmode}")


    return {
        "internship_id": itn["id"],
        "title": itn["title"],
        "slug": slug,
        "internship_type": internship_type,
        "duration": to_int(itn.get("duration")),
        "vacancy": to_int(itn.get("number_of_positions")),
        "total_positions": to_int(itn.get("total_positions")),
        "application_deadline": date.fromisoformat(itn["deadline"]) if itn["deadline"] is not None else None,
        "description": itn.get("description") or "",
        "workmode": workmode,
        "is_job_offered": to_bool(itn.get("is_job_offer")),
        "job_offered_package": str(itn["job_offer_package"]) if itn.get("job_offer_package") is not None else None,
        "city": (itn.get("city") or {}).get("name") or "",

        "company_details_page_link": (
            f"{WEBSITE_URL.rstrip('/')}/internships/{slug}"
        ),
        "application_link": (
            f"{WEBSITE_URL.rstrip('/')}"
            f"/dashboard/student/apply-to-internship/{slug}"
        ),
    }



async def fetch_page(client: httpx.AsyncClient, page: int, internship_type: str = "free"):
    async with semaphore:
        response = await client.get(
            MAIN_API_URL,
            params={
                "page": page,
                "internship_type": internship_type
            }
        )
        response.raise_for_status()

        return response.json()

async def main():
    async with httpx.AsyncClient() as client:
        tasks = []

        for query_pg in range(1, 36):
            task = asyncio.create_task(fetch_page(client, query_pg, internship_type="stipend"))
            tasks.append(task)
            if query_pg < 40:
                await asyncio.sleep(0.5)

        results = await asyncio.gather(*tasks)


        internships = []
        for page in results:
            if not page["code"] == "DATA_FOUND": continue

            main_data = page.get("data").get("data")
            for itn in main_data:
                deadline = itn.get("deadline")
                try:
                    deadline_parsed: datetime = datetime.strptime(deadline, "%Y-%m-%d")
                    if deadline_parsed.year < 2027:
                        continue
                except Exception as e:
                    print(f"invalid datetime skipping!, {e}\n Internship: {itn}")

                try:
                    internships.append(parse_internship(itn))
                except Exception as exec:
                    try:
                        print(f"Skipping internship {itn.get("id")}: {exec}")
                    except Exception as e:
                        print(itn, type(itn))

        # print(internships)
        insert_internships(internships)

        return internships

if __name__ == "__main__":
    asyncio.run(main())



