from base64 import b64encode
from uuid import uuid4, UUID

from django.db import models


class Node(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.BinaryField(blank=True)
    is_dir = models.BooleanField(default=False)
    parent = models.ForeignKey('self', models.CASCADE, null=True, related_name='children')
    previous = models.ForeignKey('self', models.CASCADE, null=True, related_name='+')
    meta = models.BinaryField(blank=True)
    size = models.IntegerField(default=0)
    blocks = models.TextField(blank=True)

    @classmethod
    def new_root(cls):
        return cls.objects.create(name=b'/', is_dir=True)

    def _list(self, prefix):
        if not self.is_dir:
            return {
                'path': b64encode(prefix + self.name).decode('ascii'),
                'is_dir': False,
                'meta': b64encode(self.meta).decode('ascii'),
                'size': self.size,
                'blocks': self.blocks.splitlines(),
            }
        if self.name == b'/':
            new_prefix = b'/'
        else:
            new_prefix = prefix + self.name + b'/'
        return {
            'path': b64encode(prefix + self.name).decode('ascii'),
            'is_dir': True,
            'meta': b64encode(self.meta).decode('ascii'),
            'children': [node.list(prefix=new_prefix) for node in self.children.all()],
        }


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    root = models.ForeignKey(Node, models.CASCADE)

    @classmethod
    def get(cls):
        uuid = UUID(int=0)
        try:
            return cls.objects.get(uuid=uuid)
        except cls.DoesNotExist:
            return cls.objects.create(uuid=uuid, root=Node.new_root())

    def find(self, path, base=b'/', create=False):
        if path.startswith(b'/'):
            node = self.root
        else:
            node = self.find(base)
        for part in path.strip(b'/').split(b'/'):
            if not part:
                continue
            try:
                node = node.children.get(name=part)
            except Node.DoesNotExist:
                if not create:
                    raise
                node = node.children.create(name=part, is_dir=True)
        return node
