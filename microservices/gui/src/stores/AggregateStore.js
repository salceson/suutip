import alt from '../alt';
import AggregateActions from '../actions/AggregateActions';
import React from 'react';

class AggregateStore {
  constructor() {
    this.searchResult = [];
    this.searchErrorMessage = null;
    this.searchLoading = false;

    this.bindListeners({
      handleSearchResult: AggregateActions.UPDATE_SEARCH,
      handleSearch: AggregateActions.SEARCH_FOR_NAME,
      handleSearchFailed: AggregateActions.SEARCH_FAILED
    });
  };

  handleSearchResult(users) {
    this.searchResult = users;
    this.searchErrorMessage = null;
    this.searchLoading = false;
  }

  handleSearch() {
    this.searchErrorMessage = null;
    this.searchResult = [];
    this.searchLoading = true;
  }

  handleSearchFailed(errorMessage) {
    this.searchErrorMessage = errorMessage;
    this.searchLoading = false;
  }
}

export default alt.createStore(AggregateStore, 'AggregateStore');
