import alt from '../alt';
import IPSource from '../sources/IPSource';

class IPActions {
  updateResult = (result) => {
    return result;
  };

  pingFailed = (errorMessage) => {
    return errorMessage;
  };

  pingHost(host) {
    return (dispatch) => {
      dispatch();
      IPSource.fetch(host)
        .then((result) => {
          this.updateResult(result)
        })
        .catch((errorMessage) => {
          this.pingFailed(errorMessage)
        });
    };
  }
}

export default alt.createActions(IPActions);
