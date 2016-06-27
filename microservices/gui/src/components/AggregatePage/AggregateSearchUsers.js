import React, {Component, PropTypes} from 'react';
import Button from '../Button';
import TextInput from '../TextInput';
import AggregateActions from '../../actions/AggregateActions';
import AggregateStore from '../../stores/AggregateStore';
import Users from './Users';
import spinner from '../spinner.gif';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './AggregatePage.scss';

class AggregateSearchUsers extends Component {

  constructor() {
    super();
    this.state = {
      name: "",
      store: AggregateStore.getState()
    };
  };

  componentDidMount() {
    AggregateStore.listen(this.onChange);
  }

  componentWillUnmount() {
    AggregateStore.unlisten(this.onChange);
  }

  onChange = (newStoreState) => {
    this.setState({store: newStoreState});
  };

  sendRequest = (event) => {
    if (this.state.name === "") return;
    AggregateActions.searchForName(this.state.name);
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
        <div>
          <form>
            <div className="form-group">
              <label htmlFor="username">User name:</label>
              <TextInput onChange={this.changeName} placeholder="User name" id="username"/>
            </div>
            <Button className="btn btn-primary" onClick={this.sendRequest}>Search</Button>
          </form>
        </div>
        <div className={s.contentContainer}>
          {content}
        </div>
      </div>
    );
  }

}

export default withStyles(AggregateSearchUsers, s);
