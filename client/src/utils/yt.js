import queryString from 'query-string';
import fetch from 'isomorphic-fetch';

const baseUrl = 'https://www.googleapis.com/youtube/v3';
const apiKey = 'AIzaSyDXaVKjKF3AK1O3KkB3ylNBpD_rOmUUxVg';

function mapItem(item) {
  return {
    id: item.id,
    title: item.snippet.title,
    channel: item.snippet.channelTitle,
    likes: item.statistics.likeCount,
    dislikes: item.statistics.dislikeCount,
    description: item.snippet.description,
    date: item.snippet.publishedAt,
    thumbnail: item.snippet.thumbnails.high || item.snippet.thumbnails.default,
  };
}

async function searchIds(params={}, key=apiKey) {
  const paramsStr = queryString.stringify({
    part: 'id',
    order: 'viewCount',
    maxResults: 20,
    ...params,
    key,
  });

  const fullUrl = `${baseUrl}/search?${paramsStr}`;

  const response = await fetch(fullUrl);
  const {items: idObjs} = await response.json();

  return idObjs.map(v => v.id.videoId);
}

export async function searchDetailsById(ids, key=apiKey) {
  const idsStr = ids.join(',');

  const detailsParamsStr = queryString.stringify({
    id: idsStr,
    part: 'snippet, statistics',
    key,
  });

  const fullDetailsUrl = `${baseUrl}/videos?${detailsParamsStr}`;
  const detailsResponse = await fetch(fullDetailsUrl);
  const {items} = await detailsResponse.json();
  return items.map(mapItem);
}

export async function search(params={}, key=apiKey) {
  const query = params.q;

  if (query.includes('youtube.com') || query.includes('youtu.be')) {
    let videoId = query.split('v=')[1];
    const ampPos = videoId.indexOf('&');

    if (ampPos != -1){
      videoId = videoId.substring(0, ampPos);
    }

    return await searchDetailsById([videoId], key);
  }

  const ids = await searchIds(params, key);
  return await searchDetailsById(ids, key);
}

