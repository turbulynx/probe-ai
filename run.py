from typing import List

from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from search import TavilySearch, Search, SerpApiSearch, Summary, SearchFactory
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
swagger = Swagger(app)
swagger.config['definitions'] = {
    'Summary': {
        'type': 'object',
        'properties': {
            'title': {
                'type': 'string',
                'description': 'Title of the search result'
            },
            'url': {
                'type': 'string',
                'description': 'URL of the search result'
            },
            'content': {
                'type': 'string',
                'description': 'Content description of the search result'
            }
        }
    }
}


@app.route('/search', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The name of the person to search for'
        },
        {
            'name': 'tags',
            'in': 'query',
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'A list of additional tags (e.g., "data scientist", "singapore")'
        },
        {
            'name': 'domains',
            'in': 'query',
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'List of domains to search in (e.g., "linkedin.com", "facebook.com")'
        },
        {
            'name': 'max_results',
            'in': 'query',
            'type': 'integer',
            'description': 'Maximum number of search results to return'
        },
        {
            'name': 'search_tool',
            'in': 'query',
            'type': 'string',
            'enum': ['tavily', 'searchapi'],
            'description': 'The search tool to use (either "tavily" or "searchapi")',
            'default': 'tavily'
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of search results',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Summary'
                }
            }
        },
        '400': {
            'description': 'Bad Request - Name parameter is required'
        }
    }
})
def search_person():
    """
    Search for a person's details by name.
    This endpoint allows you to get a list of search results with title, URL, and content
    based on the person's name and additional tags using Tavily search.

    ---
    responses:
      200:
        description: A list of search results
        schema:
          type: array
          items:
            $ref: '#/definitions/Summary'
      400:
        description: Name parameter is required
    """
    name = request.args.get('name')
    tags = request.args.getlist('tags')
    domains = request.args.getlist('domains')
    max_results = request.args.get('max_results', default=20, type=int)
    search_tool = request.args.get('max_results', default="tavily", type=str)

    if not name:
        return jsonify({"error": "Name parameter is required"}), 400

    results: List[Summary] = SearchFactory().get_search_instance(search_tool).get_results(name, tags, domains, max_results)
    results_dict = [result.to_dict() for result in results]
    return jsonify(results_dict), 200


@swag_from({
    'tags': ['Search'],
    'description': 'Get the list of all supported domains from all subclasses of Search.',
    'responses': {
        '200': {
            'description': 'List of all supported domains',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'example': 'linkedin.com'  # Example of what a source might look like
                }
            }
        },
        '400': {
            'description': 'Bad Request - something went wrong'
        }
    }
})
@app.route('/supported_domains', methods=['GET'])
def supported_domain_endpoint():
    """Endpoint to get all supported domains from subclasses of Search."""
    supported_domains = list()
    subclasses = Search.__subclasses__()
    for subclass in subclasses:
        try:
            subclass_instance = subclass()
            if hasattr(subclass_instance, 'supported_domain') and callable(getattr(subclass_instance, 'supported_domain')):
                supported_domains.append({
                    "name": subclass.__name__,
                    "supported_domains": subclass_instance.supported_domain()
                })
        except NotImplementedError:
            pass

    return jsonify(supported_domains), 200


@app.route('/health')
def swagger_ui():
    return {"status": "UP"}

if __name__ == "__main__":
    swagger.config['specs_route'] = '/'
    app.run(debug=True)

