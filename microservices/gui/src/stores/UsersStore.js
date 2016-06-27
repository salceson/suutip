import alt from '../alt';
import UsersActions from '../actions/UsersActions';
import React from 'react';

class UsersStore {
  constructor() {
    this.listResult = [];
    this.listErrorMessage = null;
    this.listLoading = false;
    this.searchResult = [];
    this.searchErrorMessage = null;
    this.searchLoading = false;
    this.addResult = null;
    this.addErrorMessage = null;
    this.addLoading = false;

    this.bindListeners({
      handleGetAllResult: UsersActions.UPDATE_LIST,
      handleGetAll: UsersActions.GET_ALL,
      handleGetAllFailed: UsersActions.LIST_FAILED,
      handleSearchResult: UsersActions.UPDATE_SEARCH,
      handleSearch: UsersActions.SEARCH_FOR_NAME,
      handleSearchFailed: UsersActions.SEARCH_FAILED,
      handleAddUserResult: UsersActions.ADD_OK,
      handleAddUser: UsersActions.ADD_USER,
      handlerAddUserFailed: UsersActions.ADD_FAILED
    });
  };

  handleGetAllResult(users) {
    this.listResult = users;
    this.listErrorMessage = null;
    this.listLoading = false;
  };

  handleGetAll() {
    this.listErrorMessage = null;
    this.listResult = []; //For spinner to be rendered
    this.listLoading = true;
  };

  handleGetAllFailed(errorMessage) {
    this.listErrorMessage = errorMessage;
    this.listLoading = false;
  }

  handleSearchResult(users) {
    this.searchResult = users;
    this.searchErrorMessage = null;
    this.searchLoading = false;
  }

  handleSearch() {
    this.searchResult = [];
    this.searchErrorMessage = null;
    this.searchLoading = true;
  }

  handleSearchFailed(errorMessage) {
    this.searchErrorMessage = errorMessage;
    this.searchLoading = false;
  }

  handleAddUserResult(result) {
    this.addResult = result;
    this.addErrorMessage = null;
    this.addLoading = false;
  }

  handleAddUser() {
    this.addResult = null;
    this.addErrorMessage = null;
    this.addLoading = true;
  }

  handlerAddUserFailed(errorMessage) {
    this.addErrorMessage = errorMessage;
    this.addLoading = false;
  }
}

export default alt.createStore(UsersStore, 'UsersStore');
