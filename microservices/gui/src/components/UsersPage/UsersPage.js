import React, {Component, PropTypes} from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './UsersPage.scss';
import AllUsers from './AllUsers';
import SearchUsers from './SearchUsers';
import AddUser from './AddUser';

class UsersPage extends Component {

  static contextTypes = {
    onSetTitle: PropTypes.func.isRequired
  };

  render() {
    const title = 'Users service';
    this.context.onSetTitle(title);

    return (
      <div className={s.root}>
        <div className={s.container}>
          <h2>{title}</h2>
          <h3>All users</h3>
          <AllUsers/>
          <h3>Search users</h3>
          <SearchUsers/>
          <h3>Add user</h3>
          <AddUser/>
        </div>
      </div>
    );
  }

}

export default withStyles(UsersPage, s);
