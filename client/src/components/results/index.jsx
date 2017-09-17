import React from 'react';
import Radium from 'radium';
import styler from 'react-styling';

@Radium
export default class Results extends React.Component  {
  render() {
    return (
      <div style={styles.results}>
        Hi
      </div>
    );
  }
}

const styles = styler`
  results
    width: 100%
    min-height: 100vh
`;
