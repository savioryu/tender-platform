import request from '@/utils/request';

export function getList(data) {
  return request({
    url: '/announcement/getList',
    method: 'post',
    data
  });
}

export function getDetail(contentId) {
  return request({
    url: `/announcement/getDetail/${contentId}`,
    method: 'get'
  });
}
