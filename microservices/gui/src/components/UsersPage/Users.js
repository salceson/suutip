import React, {Component, PropTypes} from 'react';
import User from './User';
import s from './UsersPage.scss';
import withStyles from 'isomorphic-style-loader/lib/withStyles';

class Users extends Component {
  static propTypes = {
    users: PropTypes.array
  };

  render() {
    const className = `table table-hover table-bordered table-striped ${s.resultTable}`;
    return (
      <table className={className}>
        <thead>
          <tr>
            <th>Name</th>
            <th>E-mail</th>
            <th>IP address</th>
          </tr>
        </thead>
        <tbody>
          {this.props.users.map((user) => <User key={user.id} name={user.name} ip={user.ip}
                                                email={user.email}/>)}
        </tbody>
      </table>
    );
  }
}

export default withStyles(Users, s);
