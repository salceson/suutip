/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

/* eslint-disable max-len */
/* jscs:disable maximumLineLength */

export const port = process.env.PORT || 3001;
export const hostName = process.env.WEBSITE_HOSTNAME || '0.0.0.0';
export const host = process.env.WEBSITE_HOSTNAME || `${hostName}:${port}`;
export const usersUrl = process.env.USERS_URL || 'http://localhost:5002/';
export const ipdiagUrl = process.env.IPDIAG_URL || 'http://localhost:5001/';
export const aggregateUrl = process.env.AGGREGATE_URL || 'http://localhost:5003/';
