import {combineReducers} from 'redux';
import {routerReducer} from 'react-router-redux';

import {
  INVALIDATE_SCENES, REQUEST_SCENES, RECEIVE_SCENES,
  INVALIDATE_VIDEOS, SEARCH_VIDEOS, RECEIVE_VIDEOS,
  CHANGE_VIDEO_QUERY, CLEAR_VIDEO_QUERY, CHANGE_SCENE_QUERY, CLEAR_SCENE_QUERY,
  REQUEST_SCENE_SEARCH, RECEIVE_SCENE_SEARCH,
  UPDATE_CARD_HEIGHT,
  CHANGE_PLAYER, CHANGE_TIME,
} from './actions';

function videoScenes(state = {
  isFetching: false,
  didInvalidate: false,
  items: [],
}, action) {
  switch (action.type) {
    case INVALIDATE_SCENES:
      return {...state,
        didInvalidate: true,
      };
    case REQUEST_SCENES:
      return {...state,
        isFetching: true,
        didInvalidate: false,
        items: [],
        itemsByTime: {},
      };
    case RECEIVE_SCENES:
      return {...state,
        isFetching: false,
        didInvalidate: false,
        items: action.items,
        itemsByTime: action.itemsByTime,
      };
    default:
      return state;
  }
}

function sceneSearch(state ={
  isFetching: false,
  didInvalidate: false,
  results: [],
}, action) {
  switch (action.type) {
    case REQUEST_SCENE_SEARCH:
      return {...state,
        isFetching: true,
        didInvalidate: false,
        results: [],
      };
    case RECEIVE_SCENE_SEARCH:
      return {...state,
        isFetching: false,
        didInvalidate: false,
        results: action.results,
      };
    default:
      return state;
  }
}


function videos(state = {
  isFetching: false,
  didInvalidate: false,
  items: [],
  itemsById: {},
}, action) {
  switch (action.type) {
    case INVALIDATE_VIDEOS:
      return {...state,
        didInvalidate: true,
      };
    case SEARCH_VIDEOS:
      return {...state,
        isFetching: true,
        didInvalidate: false,
      };
    case RECEIVE_VIDEOS:
      return {...state,
        isFetching: false,
        didInvalidate: false,
        items: action.items,
        itemsById: action.itemsById,
        lastUpdated: action.receivedAt,
      };
    default:
      return state;
  }
}

function ui(state = {
  videoQuery: '',
  sceneQuery: '',
}, action) {
  switch (action.type) {
    case CHANGE_VIDEO_QUERY:
      return {...state,
        videoQuery: action.videoQuery,
      };
    case CLEAR_VIDEO_QUERY:
      return {...state,
        videoQuery: '',
      };
    case CHANGE_SCENE_QUERY:
      return {...state,
        sceneQuery: action.sceneQuery,
      };
    case CLEAR_SCENE_QUERY:
      return {...state,
        sceneQuery: '',
      };
    case UPDATE_CARD_HEIGHT:
      return {...state,
        cardHeight: action.cardHeight
      };
    default:
      return state;
  }
}

function yt(state = {
  player: {},
}, action) {
  switch (action.type) {
    case CHANGE_PLAYER:
      return {...state,
        player: action.player,
      };
    case CHANGE_TIME:
      return {...state,
        time: action.time,
      };
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  videos,
  videoScenes,
  sceneSearch,
  ui,
  yt,
  routing: routerReducer,
});

export default rootReducer;

