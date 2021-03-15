from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

get_containers = reqparse.RequestParser()
get_containers.add_argument('start',type=int,required=True,help='For pagination. Current index to start from')

detect_object = reqparse.RequestParser()
detect_object.add_argument('image',type=FileStorage,location='files',required=False,help='file')
detect_object.add_argument('container_id',type=str,required=True,help='Container ID')

check_for_one = reqparse.RequestParser()
check_for_one.add_argument('container_id',type=str,required=True,help='Container ID')


add_container_two = reqparse.RequestParser()
add_container_two.add_argument('is_countable',type=bool,required=True,help='Is the item countable')
add_container_two.add_argument('name_item',type=str,required=True,help='Name of item')
add_container_two.add_argument('container_id',type=str,required=True,help='Container ID')
