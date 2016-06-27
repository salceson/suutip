import React, {Component, PropTypes} from 'react';
import Button from '../Button';
import TextInput from '../TextInput';
import UsersActions from '../../actions/UsersActions';
import UsersStore from '../../stores/UsersStore';
import Users from './Users';
import spinner from '../spinner.gif';

class SearchUsers extends Component {

  constructor() {
    super();
    this.state = {
      name: "",
      store: UsersStore.getState()
    };
  };

  componentDidMount() {
    UsersStore.listen(this.onChange);
  }

  componentWillUnmount() {
    UsersStore.unlisten(this.onChange);
  }

  onChange = (newStoreState) => {
    this.setState({store: newStoreState});
  };

  sendRequest = (event) => {
    if (this.state.name === "") return;
    UsersActions.searchForName(this.state.name);
  };

  changeName = (event, name) => {
    this.setState({name});
  };

  render() {
    let content = "";

    if (this.state.store.searchErrorMessage) {
      content = <p>{this.state.store.searchErrorMessage}</p>;
    } else if (this.state.store.searchLoading) {
      content = <p>Loading... <img src={spinner}/></p>;
    } else if (this.state.store.searchResult.length > 0) {
      content = <Users users={this.state.store.searchResult}/>
    } else {
      content = <p>No users matching specified name.</p>;
    }

    return (
      <div>
        <form>
          <div className="form-group">
            <label htmlFor="username">User name:</label>
            <TextInput onChange={this.changeName} placeholder="User name" id="username"/>
          </div>
          <Button className="btn btn-primary" onClick={this.sendRequest}>Search</Button>
        </form>
        {content}
      </div>
    );
  }

}

export default SearchUsers;
