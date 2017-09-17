import React from 'react';
import Radium, {Style} from 'radium';
import {Route, Switch} from 'react-router';
import styler from 'react-styling';

import {Home, Results} from './components';

export default class App extends React.Component {
  render() {
    return (
      <div style={styles.app}>
        <Style rules={styles.appRules}/>
        <Switch>
          <Route exact path='/' component={Home}/>
          <Route path='/results' component={Results}/>
        </Switch>
        {this.props.children}
      </div>
    );
  }
}

const styles = styler`
  app
    background: rgba(0,0,0,0.03)
    font-family: 'mr-eaves-xl-sans', sans-serif
    font-size: 17px
    letter-spacing: 0.4px
    line-height: 1.5em
    color: rgba(24,50,80,1)
    display: flex
    flex-direction: column
    align-items: center
    justify-content: center
    min-height: 100vh

  appRules 
    *
      box-sizing: border-box
    a
      color: rgba(24,50,80,1)

    ::-webkit-input-placeholder
      color: rgba(255,255,255,0.5)
`;
