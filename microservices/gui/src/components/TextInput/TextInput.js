import React, {Component, PropTypes} from 'react';

class TextInput extends Component {
  static propTypes = {
    onChange: PropTypes.func
  };

  handleChange = (event) => {
    event.preventDefault();
    const handler = this.props.onChange;
    if (handler) {
      handler(event, event.target.value);
    }
  };

  render() {
    const {onChange, ...props} = this.props;
    return <input className="form-control" type="text" onChange={this.handleChange} {...props}/>;
  }
}

export default TextInput;
