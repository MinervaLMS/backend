from rest_framework import serializers

from ..models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_name",
            "parent_comment_id",
            "post_date",
            "content",
            "fixed",
            "replies",
        ]

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment_id=obj.id)

        if replies.exists():
            return CommentSerializer(replies, many=True).data

        return None

    def get_user_name(self, obj):
        return obj.user_id.get_full_name()
