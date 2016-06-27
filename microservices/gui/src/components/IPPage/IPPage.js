import React, {Component, PropTypes} from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './IPPage.scss';
import Button from '../Button';
import TextInput from '../TextInput';
import IPActions from '../../actions/IPActions';
import IPStore from '../../stores/IPStore';
import spinner from '../spinner.gif';

class IPPage extends Component {

  static contextTypes = {
    onSetTitle: PropTypes.func.isRequired
  };

  constructor() {
    super();
    this.state = {
      ip: "",
      store: IPStore.getState()
    };
  };

  componentDidMount() {
    IPStore.listen(this.onChange);
  }

  componentWillUnmount() {
    IPStore.unlisten(this.onChange);
  }

  onChange = (newStoreState) => {
    this.setState({store: newStoreState});
  };

  sendRequest = (event) => {
    if (this.state.ip !== "") {
      IPActions.pingHost(this.state.ip);
    }
  };

  updateIP = (event, ip) => {
    this.setState({ip});
  };

  render() {
    const title = 'IP Diagnostics Service';
    this.context.onSetTitle(title);

    let content = "";

    if (this.state.store.errorMessage) {
      content = <div>{this.state.store.errorMessage}</div>;
    } else if (this.state.store.loading) {
      content = (
        <div>
          <p>Loading... <img src={spinner}/></p>
        </div>
      );
    } else {
      content = <div>{this.state.store.ipResult}</div>;
    }

    return (
      <div className={s.root}>
        <div className={s.container}>
          <h1>{title}</h1>
          <p>Please enter host IP to run diagnostics:</p>
          <div>
            <form>
              <div className="form-group">
                <label htmlFor="ip">IP to ping:</label>
                <TextInput onChange={this.updateIP} placeholder="IP to ping" id="ip"/>
              </div>
              <Button className="btn btn-primary" onClick={this.sendRequest}>Send ping!</Button>
            </form>
          </div>
          <h2>Response:</h2>
          <div>
            {content}
          </div>
        </div>
      </div>
    );
  }

}

export default withStyles(IPPage, s);
