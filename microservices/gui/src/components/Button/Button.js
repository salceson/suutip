import React, {Component, PropTypes} from 'react';

class Button extends Component {
  static propTypes = {
    onClick: PropTypes.func
  };

  handleClick = (event) => {
    event.preventDefault();
    const handler = this.props.onClick;
    if (handler) {
      handler(event);
    }
  };

  render() {
    const {onClick, ...props} = this.props;
    return <button onClick={this.handleClick} {...props}/>;
  }
}

export default Button;
