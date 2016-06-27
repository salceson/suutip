import React, {Component, PropTypes} from 'react';
import User from './User';

class Users extends Component {
  static propTypes = {
    users: PropTypes.array
  };

  render() {
    return (
      <table className="table table-hover table-bordered table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>E-mail</th>
            <th>IP address</th>
            <th>Ping result</th>
          </tr>
        </thead>
        <tbody>
          {this.props.users.map(({user, diagnostic}) => <User key={user.id}
                                                              name={user.name}
                                                              ip={user.ip}
                                                              email={user.email}
                                                              ipdiag={diagnostic.ping_result}/>)}
        </tbody>
      </table>
    );
  }
}

export default Users;
