import React from 'react';
import $ from 'jquery';
import {usersUrl} from '../config';

class UsersSource {
  fetchAll = () => {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: `${usersUrl}users`
      })
        .done((data) => {
          if (data.users !== undefined) {
            resolve(data.users)
          } else {
            reject('Failed to fetch users from database!');
          }
        })
        .fail((xhr) => {
          reject('Could not connect to server!')
        });
    });
  };

  search = (name) => {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: `${usersUrl}users/name/${name}`
      })
        .done((data) => {
          if (data.users !== undefined) {
            resolve(data.users)
          } else {
            reject('Failed to fetch users from database!');
          }
        })
        .fail((xhr) => {
          reject('Could not connect to server!')
        });
    });
  };

  addUser = (user) => {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: 'POST',
        url: `${usersUrl}users`,
        contentType: 'application/json',
        data: JSON.stringify(user)
      })
        .done((data) => {
          resolve(`Successfully added user ${user.name}`)
        })
        .fail((xhr) => {
          if (xhr.responseText) {
            const parsed = JSON.parse(xhr.responseText);
            reject(parsed.message);
          } else {
            reject('Could not connect to server!');
          }
        });
    });
  };
}

export default new UsersSource();
