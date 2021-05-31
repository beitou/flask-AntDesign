
from app import db
from app.utils import make_qrcode
from app.utils import query_to_dict
from app.treasure.models import Treasure


class Service():

    def create(self, data):
        """
        :param data:
        :return:
        """
        # 生成二维码
        img = make_qrcode(data['url'])
        data.setdefault('image', img)
        # 将数据存入数据库
        model = Treasure(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

    def search(self, data):
        """
        :param data:
        :return:
        """
        if 'id' in data and data['id']:
            model = Treasure.query.get(data['id'])
            return 1, model.to_dict()

        filter = {}

        if 'name' in data and data['name'] and data['name'] != 'all':
            filter.setdefault('name', data.get('name'))

        if 'type' in data and data['type'] and data['type'] != 'all':
            filter.setdefault('type', data.get('type'))

        if 'platform' in data and data['platform'] and data['platform'] != 'all':
            filter.setdefault('platform', data.get('platform'))

        try:
            offset = int(data.get('pager', 1)) - 1
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('size', 10))
        except TypeError:
            limit = 10
        print(filter, offset, limit)
        results = Treasure.query.filter_by(
            **filter
        ).order_by(
            Treasure.created.desc()
        ).offset(offset).limit(limit)

        results = query_to_dict(results)
        count = Treasure.query.filter_by(**filter).count()
        return count, results
