import alt from '../alt';
import UsersSource from '../sources/UsersSource';

class UsersActions {
  updateList = (result) => {
    return result;
  };

  listFailed = (errorMessage) => {
    return errorMessage;
  };

  getAll() {
    return (dispatch) => {
      dispatch();
      UsersSource.fetchAll()
        .then((result) => {
          this.updateList(result)
        })
        .catch((errorMessage) => {
          this.listFailed(errorMessage)
        });
    };
  }

  updateSearch = (result) => {
    return result;
  };

  searchFailed = (errorMessage) => {
    return errorMessage;
  };

  searchForName(name) {
    return (dispatch) => {
      dispatch();
      UsersSource.search(name)
        .then((result) => {
          this.updateSearch(result)
        })
        .catch((errorMessage) => {
          this.searchFailed(errorMessage)
        });
    };
  }

  addOk = (result) => {
    return result;
  };

  addFailed = (errorMessage) => {
    return errorMessage;
  };

  addUser(user) {
    return (dispatch) => {
      dispatch();
      UsersSource.addUser(user)
        .then((result) => {
          this.addOk(result);
          this.getAll();
        })
        .catch((errorMessage) => {
          this.addFailed(errorMessage)
        });
    };
  }
}

export default alt.createActions(UsersActions);
