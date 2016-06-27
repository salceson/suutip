import React, {Component, PropTypes} from 'react';

class User extends Component {
  static propTypes = {
    name: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    ip: PropTypes.string.isRequired,
    ipdiag: PropTypes.string.isRequired
  };

  render() {
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.props.email}</td>
        <td>{this.props.ip}</td>
        <td><pre>{this.props.ipdiag}</pre></td>
      </tr>
    );
  }
}

export default User;
