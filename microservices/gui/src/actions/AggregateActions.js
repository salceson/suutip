import alt from '../alt';
import AggregateSource from '../sources/AggregateSource';

class AggregateActions {
  updateSearch = (result) => {
    return result;
  };

  searchFailed = (errorMessage) => {
    return errorMessage;
  };

  searchForName(name) {
    return (dispatch) => {
      dispatch();
      AggregateSource.search(name)
        .then((result) => {
          this.updateSearch(result)
        })
        .catch((errorMessage) => {
          this.searchFailed(errorMessage)
        });
    };
  }
}

export default alt.createActions(AggregateActions);
