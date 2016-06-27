import alt from '../alt';
import IPActions from '../actions/IPActions';
import React from 'react';

class IPStore {
  constructor() {
    this.ipResult = <pre>Please send request first!</pre>;
    this.errorMessage = null;
    this.loading = false;

    this.bindListeners({
      handleResult: IPActions.UPDATE_RESULT,
      handlePing: IPActions.PING_HOST,
      handlePingFailed: IPActions.PING_FAILED
    });
  };

  handleResult(ipResult) {
    this.ipResult = ipResult;
    this.errorMessage = null;
    this.loading = false;
  };

  handlePing() {
    this.loading = true;
    this.errorMessage = null;
    this.ipResult = "";
  };

  handlePingFailed(errorMessage) {
    this.loading = false;
    this.errorMessage = errorMessage;
  }
}

export default alt.createStore(IPStore, 'IPStore');
