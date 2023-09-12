from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.comment import Comment
from accounts.models.user import User
from courses.models.material import Material
from ..serializers.comment_serializer import CommentSerializer
from ..schemas import comment_schemas as schemas
from courses.helpers.enrollment_validate import validate_enrollment


@api_view(["POST"])
@schema(schemas.create_comment_schema)
@permission_classes([IsAuthenticated])
def create_comment(request) -> JsonResponse:
    """Create a comment in a material by a user.

    Args:
        request: request http with comment data
        {
            "material_id": int,
            "user_id": int,
            "parent_comment_id": int,
            "content": str
        }
    Returns:
        JsonResponse: HTTP response in JSON format with the comment data
    """
    try:
        material: Material = Material.objects.get(id=request.data["material_id"])
        user: User = User.objects.get(id=request.data["user_id"])
        # Verify if the user is enrolled in the course to which the material belongs
        if not validate_enrollment(user.id, material.id):
            return JsonResponse(
                {"message": "You do not have permission to comment this material"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Create the comment
        comment: Comment = CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            material.total_comments += 1
            material.save()
            return JsonResponse(
                data=comment.data,
                safe=False,
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(
            data=comment.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@schema(schemas.get_comment_schema)
@permission_classes([IsAuthenticated])
def get_comment(request, comment_id: int) -> JsonResponse:
    """Get a comment by its id

    Args:
        request : request http
        comment_id (int): Comment's id to get

    Returns:
        JsonResponse: JSON response with the comment data
    """
    try:
        comment: Comment = Comment.objects.get(id=comment_id)
        comment = CommentSerializer(comment)
        return JsonResponse(comment.data, safe=False, status=status.HTTP_200_OK)

    except Comment.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an comment with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@schema(schemas.get_comment_replies_schema)
@permission_classes([IsAuthenticated])
def get_comment_replies(request, comment_id: int) -> JsonResponse:
    """Get all replies of a comment

    Args:
        request : request http
        comment_id (int): Comment's id to get its replies

    Returns:
        JsonResponse: JSON response with the list of replies
    """
    try:
        comment: Comment = Comment.objects.get(id=comment_id)
        replies = comment.comment_set.all()

        if replies:
            replies = CommentSerializer(replies, many=True)
            return JsonResponse(replies.data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            data={"message": "This comment has not replies"},
            status=status.HTTP_200_OK,
        )

    except Comment.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an comment with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_material_comments(request, material_id: int) -> JsonResponse:
    """Get all comments of a material in a
    data structure with the replies of each comment

    Args:
        request: HTTP request
        material_id (int): Material's id to get its comments

    Returns:
        JsonResponse: HTTP response in JSON format with the comments data
    """

    try:
        comments: Comment = Comment.objects.filter(
            material_id=material_id, parent_comment_id=None
        )
        ordered_comments = comments.order_by("fixed", "-post_date")

        serialized_comments = CommentSerializer(ordered_comments, many=True)
        return JsonResponse(
            serialized_comments.data, safe=False, status=status.HTTP_200_OK
        )

    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["DELETE"])
@schema(schemas.delete_comment_schema)
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id: int) -> JsonResponse:
    """Delete a comment by its id

    Args:
        request: request http
        comment_id (int): Comment's id to delete

    Returns:
        JsonResponse: JSON response with the confirmation of the delete
    """
    try:
        comment: Comment = Comment.objects.get(id=comment_id)
        # Decrease the total comments of the material
        material: Material = comment.material_id
        material.total_comments -= 1
        material.save()
        comment.delete()

        return JsonResponse(
            data={"message": "Comment deleted successfully"},
            status=status.HTTP_200_OK,
        )

    except Comment.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not an comment with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


# TODO: These views below should be in accounts app


@api_view(["GET"])
@schema(schemas.get_user_comments_schema)
@permission_classes([IsAuthenticated])
def get_user_comments(request, user_id: int, material_id: int) -> JsonResponse:
    """Get all comments of a user in a material

    Args:
        request : request http
        user_id (int): User's id to get its comments
        material_id (int): Material's id to get its comments

    Returns:
        JsonResponse:
        JSON response with the list of comments done by the user in the material
    """
    try:
        user: User = User.objects.get(id=user_id)
        user_comments = user.comment_set.filter(material_id=material_id)
        if user_comments:
            user_comments = CommentSerializer(user_comments, many=True)
            return JsonResponse(
                user_comments.data, safe=False, status=status.HTTP_200_OK
            )

        return JsonResponse(
            data={"message": "This user does not have comments in this material"},
            status=status.HTTP_200_OK,
        )

    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@schema(schemas.update_user_comment_schema)
@permission_classes([IsAuthenticated])
def update_user_comment(request, user_id: int, comment_id: int) -> JsonResponse:
    """Update a comment done by a user

    Args:
        request : request http with the new content of the comment
        user_id (int): User's id who did the comment
        comment_id (int): Comment's id to update

    Returns:
        JsonResponse: JSON response with the confirmation of the update
    """
    try:
        user: User = User.objects.get(pk=user_id)
        comment_by_user: Comment = user.comment_set.get(pk=comment_id)

        if "content" not in request.data:
            return JsonResponse(
                data={"message": "Content is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment_by_user.content = request.data["content"]
        comment_by_user.save()
        return JsonResponse(
            data={"message": "Comment updated successfully"},
            status=status.HTTP_200_OK,
        )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not an user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Comment.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a comment with this id for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["DELETE"])
@schema(schemas.delete_user_comment_schema)
@permission_classes([IsAuthenticated])
def delete_user_comment(request, user_id: int, comment_id: int) -> JsonResponse:
    """Delete a comment done by a user

    Args:
        request : request http
        user_id (int): User's id who did the comment
        comment_id (int): Comment's id to delete

    Returns:
        JsonResponse: Json response with the confirmation of the delete
    """
    try:
        user: User = User.objects.get(pk=user_id)
        comment_to_delete: Comment = user.comment_set.get(pk=comment_id)
        # Decrease the total comments of the material
        material: Material = comment_to_delete.material_id
        material.total_comments -= 1
        material.save()
        comment_to_delete.delete()
        return JsonResponse(
            data={"message": "Comment deleted successfully"},
            status=status.HTTP_200_OK,
        )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not an user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Comment.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a comment with this id for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )
