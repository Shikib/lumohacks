import queryString from 'query-string';
import fetch from 'isomorphic-fetch';

import {search} from '../utils/yt';

export const INVALIDATE_SCENES = 'INVALIDATE_SCENES';
export const REQUEST_SCENES = 'REQUEST_SCENES';
export const RECEIVE_SCENES = 'RECEIVE_SCENES';

export const INVALIDATE_VIDEOS = 'INVALIDATE_VIDEOS';
export const SEARCH_VIDEOS = 'SEARCH_VIDEOS';
export const RECEIVE_VIDEOS = 'RECEIVE_VIDEOS';

export const CHANGE_VIDEO_QUERY = 'CHANGE_VIDEO_QUERY';
export const CLEAR_VIDEO_QUERY = 'CLEAR_VIDEO_QUERY';
export const CHANGE_SCENE_QUERY = 'CHANGE_SCENE_QUERY';
export const CLEAR_SCENE_QUERY = 'CLEAR_SCENE_QUERY';

export const REQUEST_SCENE_SEARCH = 'REQUEST_SCENE_SEARCH';
export const RECEIVE_SCENE_SEARCH = 'RECEIVE_SCENE_SEARCH';

export const UPDATE_CARD_HEIGHT = 'UPDATE_CARD_HEIGHT';

export const CHANGE_PLAYER = 'CHANGE_PLAYER';
export const CHANGE_TIME = 'CHANGE_TIME';

export function searchVideos(query) {
  return {
    type: SEARCH_VIDEOS,
    query,
  };
}

export function receiveVideos(items) {
  const itemsById = {};

  items.forEach(v => {
    itemsById[v.id] = v;
  });

  return {
    type: RECEIVE_VIDEOS,
    items,
    itemsById,
    receivedAt: Date.now(),
  };
}

export function fetchVideos(query) {
  return async dispatch => {
    if (query == '') {
      return dispatch(receiveVideos([]));
    }
    dispatch(searchVideos(query));
    const items = await search({q: query});
    dispatch(receiveVideos(items));
  };
}

export function requestScenes(videoId) {
  return {
    type: REQUEST_SCENES,
    videoId,
  };
}

export function receiveScenes(items, itemsByTime) {
  return {
    type: RECEIVE_SCENES,
    items,
    itemsByTime,
    receivedAt: Date.now(),
  };
}

export function requestSceneSearch(videoId, query) {
  return {
    type: REQUEST_SCENE_SEARCH,
    videoId,
    query,
  };
}

export function receiveSceneSearch(results) {
  return {
    type: RECEIVE_SCENE_SEARCH,
    results,
  };
}

export function fetchScenes(videoId) {
  const url = 'http://40.83.188.31:8080/build/' + videoId;
  return async dispatch => {
    dispatch(requestScenes(videoId));
    const response = await fetch(url);
    const json = await response.json();  
    const scenes = json.scenes.map(scene => ({
      ...scene,
      image: 'data:image/jpeg;base64,' + scene.image,
    }));

    const scenesByTime = {};

    scenes.forEach(scene => {
      scenesByTime[scene.time] = scene;
    });

    dispatch(receiveScenes(scenes, scenesByTime));
  };
}

export function fetchSceneSearch(videoId, query) {
  const baseUrl = 'http://40.83.188.31:8080';
  const paramsStr = queryString.stringify({
    video_id: videoId,
    search_term: query,
  }); 
  const fullUrl = `${baseUrl}/search/?${paramsStr}`;

  return async dispatch => {
    dispatch(requestSceneSearch(videoId, query));
    const response = await fetch(fullUrl);
    let json
    if (response.status == 200) {
      json = await response.json();
    } else {
      json = []
    }

    dispatch(receiveSceneSearch(json));
  };
};

export function changeVideoQuery(videoQuery) {
  return {
    type: CHANGE_VIDEO_QUERY,
    videoQuery,
  };
    console.log(json);
}

export function clearVideoQuery() {
  return {
    type: CLEAR_VIDEO_QUERY,
    videoQuery: '',
  };
}

export function changeSceneQuery(sceneQuery) {
  return {
    type: CHANGE_SCENE_QUERY,
    sceneQuery,
  };
}

export function clearSceneQuery(sceneQuery) {
  return {
    type: CLEAR_SCENE_QUERY,
    sceneQuery: '',
  };
}

export function updateCardHeight(cardHeight) {
  return {
    type: UPDATE_CARD_HEIGHT,
    cardHeight,
  };
}

export function changePlayer(player) {
  return {
    type: CHANGE_PLAYER,
    player,
  };
}

export function changeTime(time) {
  return {
    type: CHANGE_TIME,
    time,
  };
}

