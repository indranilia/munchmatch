import { createLoading, removeLoading } from "./_helper.js";

export async function post(url, body, fullPath = false, stopLoading = true) {
  try {
    createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(newUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await query.json();
    const status = query.status;

    if (stopLoading) removeLoading();
    return { status, data };
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

export async function get(url, fullPath = false, stopLoading = true) {
  try {
    createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(newUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await query.json();
    const status = query.status;

    if (stopLoading) removeLoading();
    return { status, data };
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

export async function patch(url, body, fullPath = false, stopLoading = true) {
  try {
    createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(newUrl, {
      method: "PATCH",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    if (stopLoading) removeLoading();
    return status;
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}

export async function remove(url, item, fullPath = false, stopLoading = true) {
  try {
    createLoading();
    const newUrl = fullPath ? url : `${window.location.origin}${url}`;
    const query = await fetch(`${newUrl}/${item}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    if (stopLoading) removeLoading();
    return status;
  } catch (error) {
    if (stopLoading) removeLoading();
    throw new Error(error.message);
  }
}
