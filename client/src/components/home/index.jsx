import React from 'react';
import Radium from 'radium';
import styler from 'react-styling';

@Radium
export default class Home extends React.Component {
  render() {
    return (
      <div style={styles.home}>
        <div style={styles.homeContainer}>
          <h1 style={styles.heading}>
            Concerned for a friend?
          </h1>
          <p style={styles.caption}>
            Help a Friend will check your friend's social media history for signs of depression, and suggest helpful resources if they appear to be at risk.
          </p>
          <div style={styles.socialBox}>
            <div style={styles.socialIcon.reddit}/> 
            <div style={styles.socialLabel}>Reddit</div>
            <input
              type='text'
              style={styles.redditInput}
              placeholder={'Username'}/>
            <div style={styles.clearfix}/>
          </div>
          <div style={styles.socialBox}>
            <div style={styles.socialIcon.twitter}/> 
            <div style={styles.socialLabel}>Twitter</div>
            <input
              type='text'
              style={styles.redditInput}
              placeholder={'Username'}/>
            <div style={styles.clearfix}/>
          </div>
          <button style={styles.socialSubmit}>
            <div style={styles.arrowIcon}/> 
            Check
          </button>
        </div>
      </div>
    );
  }
}

const styles = styler`
  home
    color: #fff
    background: linear-gradient(to bottom, #f2825b 0%,#e55b2b 50%,#f07146 100%)
    width: 100%
    display: flex
    flex-direction: column
    align-items: center
    justify-content: center
    min-height: 100vh

  homeContainer

  heading
    font-weight: bold
    margin-bottom: 8px
    font-size: 24px

  caption
    font-size: 13px
    line-height: 19px
    width: 500px
    margin-bottom: 24px

  socialBox
    line-height: 36px
    margin-bottom: 6px

  socialLabel
    float: left
    width: 50px
    margin-left: 6px

  socialIcon
    float: left
    background-size: 24px 24px
    background-repeat: no-repeat
    background-position: center
    width: 24px
    height: 36px

    &reddit
      background-image: url(${require('../../images/reddit-icon.svg')})

    &twitter
      background-image: url(${require('../../images/twitter-icon.svg')})

  arrowIcon
    float: left
    background-size: 18px 18px
    background-repeat: no-repeat
    background-position: center
    width: 15px
    height: 18px
    margin-right: 8px
    background-image: url(${require('../../images/arrow.svg')})

  socialSubmit
    font-weight: bold
    color: #f2825b
    margin-top: 24px
    border: none
    background: #fff
    border-radius: 9999px
    display: block
    font-family: inherit
    font-size: inherit
    padding: 8px 14px 8px 8px

  redditInput
    font-family: inherit
    font-size: inherit
    padding: 9px 0 6px
    margin-left: 16px
    background: none
    border-top: none
    border-left: none
    border-right: none
    border-bottom: 1px solid rgba(255,255,255,0.4)
    outline: none
    color: #fff
    float: left

  clearfix
    clear: both
`;
