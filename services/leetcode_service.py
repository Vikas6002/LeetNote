# services/leetcode_service.py
import requests

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

def fetch_problem_by_slug(title_slug):
    """
    Fetch problem details from LeetCode's unofficial GraphQL API.
    Input  : title_slug  e.g. "two-sum"
    Output : dict with title, difficulty, tags, problem_number
    """
    query = """
    query getQuestion($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            difficulty
            topicTags {
                name
                slug
            }
            content
            exampleTestcases
        }
    }
    """
    headers = {
        "Content-Type"  : "application/json",
        "Referer"       : "https://leetcode.com",
        "User-Agent"    : "Mozilla/5.0",
    }
    payload = {
        "query"    : query,
        "variables": {"titleSlug": title_slug},
    }

    try:
        response = requests.post(
            LEETCODE_GRAPHQL_URL,
            json    = payload,
            headers = headers,
            timeout = 10,
        )
        response.raise_for_status()
        data = response.json()

        question = data["data"]["question"]

        return {
            "problem_number": int(question["questionId"]),
            "title"         : question["title"],
            "difficulty"    : question["difficulty"].lower(),  # easy/medium/hard
            "tags"          : [t["name"] for t in question["topicTags"]],
            "content"       : question["content"],
        }

    except requests.exceptions.RequestException as e:
        print(f"LeetCode API error: {e}")
        return None

    except (KeyError, TypeError) as e:
        print(f"LeetCode response parse error: {e}")
        return None


def slug_from_url(problem_url):
    """
    Extract slug from a LeetCode URL.
    Input  : "https://leetcode.com/problems/two-sum/description/"
    Output : "two-sum"
    """
    # strip trailing slash then split
    parts = problem_url.rstrip("/").split("/")
    try:
        idx = parts.index("problems")
        return parts[idx + 1]
    except (ValueError, IndexError):
        return None