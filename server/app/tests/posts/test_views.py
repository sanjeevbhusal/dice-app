from flask import url_for

from server import PostResponseSchema


class TestPosts:
    def test_create_post(self, client):
        payload = {"title": "Test Title", "content": "Test Content"}
        response = client.post(url_for("posts.create_post"), data=payload)
        assert response.status_code == 201

    def test_get_all_posts(self, client):
        response = client.get(url_for("posts.get_all_posts"))
        assert response.status_code == 200
        assert len(response.get_json()) == 1

    def test_get_post_by_id(self, client):
        def validate_response_data(response_data):
            return PostResponseSchema().load(response_data)

        response = client.get(url_for("posts.get_post_by_id", post_id=1))
        response_data = response.get_json().get("post")
        assert response.status_code == 200
        assert validate_response_data(response_data)

    def test_update_post(self, client):
        payload = {"title": "Updated Test Title", "content": "Updated Test Content"}
        response = client.put(url_for("posts.update_post", post_id=1), data=payload)
        assert response.status_code == 200

    def test_delete_post(self, client):
        response = client.delete(url_for("posts.delete_post", post_id=1))
        assert response.status_code == 200
