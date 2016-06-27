import React, {Component, PropTypes} from 'react';
import Button from '../Button';
import UsersActions from '../../actions/UsersActions';
import UsersStore from '../../stores/UsersStore';
import Users from './Users';
import spinner from '../spinner.gif';

class AllUsers extends Component {

  constructor() {
    super();
    this.state = UsersStore.getState();
  };

  componentDidMount() {
    UsersStore.listen(this.onChange);
    UsersActions.getAll();
  }

  componentWillUnmount() {
    UsersStore.unlisten(this.onChange);
  }

  onChange = (newStoreState) => {
    this.setState(newStoreState);
  };

  sendRequest = (event) => {
    UsersActions.getAll();
  };

  render() {
    let content = "";

    if (this.state.listErrorMessage) {
      content = <p>{this.state.listErrorMessage}</p>;
    } else if (this.state.listLoading) {
      content = <p>Loading... <img src={spinner}/></p>;
    } else if (this.state.listResult.length > 0) {
      content = <Users users={this.state.listResult}/>
    } else {
      content = <p>No users.</p>;
    }

    return (
      <div>
        {content}
        <Button className="btn btn-primary" onClick={this.sendRequest}>Fetch users</Button>
      </div>
    );
  }

}

export default AllUsers;
