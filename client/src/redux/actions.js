import queryString from 'query-string';
import fetch from 'isomorphic-fetch';

export const REQUEST_DEPRESSION = 'REQUEST_DEPRESSION';
export const RECEIVE_DEPRESSION= 'RECEIVE_DEPRESSION';


export function requestDepression(reddit_handler, twitter_handler) {
  return {
    type: REQUEST_DEPRESSION,
    reddit_handler,
    twitter_handler,
  };
}

export function receiveDepression(results) {
  return {
    type: RECEIVE_DEPRESSION,
    results,
    receivedAt: Date.now(),
  };
}

export function fetchDepression(reddit_handler, twitter_handler) {
  const baseUrl = 'http://40.83.188.31:8080'; // TODO
  const paramsStr = queryString.stringify({
    reddit_handler: reddit_handler,
    twitter_handler: twitter_handler,
  }); 
  const fullUrl = `${baseUrl}/analyze/?${paramsStr}`;

  return async dispatch => {
    dispatch(requestDepression(reddit_handler, twitter_handler));
    const response = await fetch(url);
    const results = await response.json();
    dispatch(receiveDepression(results));