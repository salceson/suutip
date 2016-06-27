import React, {Component, PropTypes} from "react";
import Button from "../Button";
import TextInput from "../TextInput";
import UsersActions from "../../actions/UsersActions";
import UsersStore from "../../stores/UsersStore";
import spinner from "../spinner.gif";

class AddUser extends Component {

  constructor() {
    super();
    this.state = {
      name: "",
      email: "",
      ip: "",
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
    if (this.state.name === "" || this.state.ip === "" || this.state.email === "") return;
    UsersActions.addUser({
      name: this.state.name,
      email: this.state.email,
      ip: this.state.ip
    });
  };

  changeName = (event, name) => {
    this.setState({name});
  };

  changeEmail = (event, email) => {
    this.setState({email});
  };

  changeIP = (event, ip) => {
    this.setState({ip});
  };

  render() {
    let content = null;

    if (this.state.store.addErrorMessage) {
      content = <p>{this.state.store.addErrorMessage}</p>;
    } else if (this.state.store.addLoading) {
      content = <p>Loading... <img src={spinner}/></p>;
    } else if (this.state.store.addResult) {
      content = <p>{this.state.store.addResult}</p>
    }

    return (
      <div>
        <p>User name and user e-mail must be unique!</p>
        <form>
          <div className="form-group">
            <label htmlFor="username">User name:</label>
            <TextInput onChange={this.changeName} placeholder="User name"/>
          </div>
          <div className="form-group">
            <label htmlFor="email">User email:</label>
            <TextInput onChange={this.changeEmail} placeholder="User email" id="email"/>
          </div>
          <div className="form-group">
            <label htmlFor="ip">User IP address:</label>
            <TextInput onChange={this.changeIP} placeholder="User IP address" id="ip"/>
          </div>
          <Button className="btn btn-primary" onClick={this.sendRequest}>Add user</Button>
        </form>
        {content}
      </div>
    );
  }

}

export default AddUser;
