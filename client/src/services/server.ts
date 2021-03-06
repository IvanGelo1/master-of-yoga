import { auth } from './firebase';
import axios, { AxiosResponse } from 'axios';
import { UserDTO } from '../interfaces/UserDTO';
import { BaseRoutinesDTO } from '../interfaces/RoutineDTO';
import { AuthResponseDTO } from '../interfaces/AuthResponseDTO';

let baseUrl: string;
const { REACT_APP_SERVER_ADDRESS } = process.env;
if (REACT_APP_SERVER_ADDRESS) {
  baseUrl = REACT_APP_SERVER_ADDRESS;
  console.log(baseUrl);
}

async function getRoutines(): Promise<BaseRoutinesDTO> {
  try {
    const routines: AxiosResponse = await axios.get(
      `${baseUrl}/api/routines/getAll`
    );
    return routines.data;
  } catch (error) {
    throw new Error(error);
  }
}

async function authUser(token: string): Promise<AuthResponseDTO> {
  try {
    const user = await axios.post(`${baseUrl}/api/users/verify`, {
      token: token,
    });
    return user.data;
  } catch (error) {
    throw new Error(error);
  }
}

async function createUser(newUser: Partial<UserDTO>): Promise<UserDTO> {
  try {
    const response: AxiosResponse = await axios.post(
      `${baseUrl}/api/users`,
      newUser
    );
    return response.data;
  } catch (error) {
    throw new Error(error);
  }
}

async function updateUserInfo(info: Partial<UserDTO>): Promise<UserDTO> {
  try {
    const uid = auth.currentUser?.uid;
    const response: AxiosResponse = await axios.post(
      `${baseUrl}/api/users/${uid}`,
      info
    );
    return response.data;
  } catch (error) {
    throw new Error(error);
  }
}

export { createUser, authUser, updateUserInfo, getRoutines };
