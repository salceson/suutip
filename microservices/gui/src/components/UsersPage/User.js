import React, {Component, PropTypes} from 'react';

class User extends Component {
  static propTypes = {
    name: PropTypes.string,
    email: PropTypes.string,
    ip: PropTypes.string
  };

  render() {
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.props.email}</td>
        <td>{this.props.ip}</td>
      </tr>
    );
  }
}

export default User;
