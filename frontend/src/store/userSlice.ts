import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UserState {
  id: string
  username: string
  password: string
  email: string
  agentStyle: string
}


const initialState: UserState = {
  id: '',
  username: '',
  password: '',
  email: '',
  agentStyle: 'Casual',
}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    // Set user info
    setUser(state, action: PayloadAction<UserState>) {
      return action.payload
    },
    
    setId(state, action: PayloadAction<string>) {
      state.id = action.payload
    },
    setUsername(state, action: PayloadAction<string>) {
      state.username = action.payload
    },
    setPassword(state, action: PayloadAction<string>) {
      state.password = action.payload
    },
    setEmail(state, action: PayloadAction<string>) {
      state.email = action.payload
    },
    setAgentStyle(state, action: PayloadAction<string>) {
      state.agentStyle = action.payload
    },
  },
})


export const { 
  setUser, 
  setId, 
  setUsername, 
  setPassword, 
  setEmail, 
  setAgentStyle 
} = userSlice.actions

// 导出 reducer
export default userSlice.reducer
