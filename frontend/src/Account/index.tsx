import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import {
  setUsername,
  setEmail,
  setPassword,
  setAgentStyle,
} from '../store/userSlice'

const Account: React.FC = () => {
  const dispatch = useDispatch()
  const [username, changeUsername] = useState('')
  const [password, changePassword] = useState('')
  const [email, changeEmail] = useState('')
  const [agentStyle, changeAgentStyle] = useState('Casual')

  const handleSave = () => {
    dispatch(setUsername(username))
    dispatch(setPassword(password))
    dispatch(setEmail(email))
    dispatch(setAgentStyle(agentStyle))
  }

  return (
    <div>
      <h2>Set Up Your Agent</h2>
      <div>
        <label>Username: </label>
        <input
          value={username}
          onChange={(e) => changeUsername(e.target.value)}
        />
      </div>
      <div>
        <label>Password: </label>
        <input
          type="password"
          value={password}
          onChange={(e) => changePassword(e.target.value)}
        />
      </div>
      <div>
        <label>Email: </label>
        <input
          value={email}
          onChange={(e) => changeEmail(e.target.value)}
        />
      </div>
      <div>
        <label>Agent Style: </label>
        <select
          value={agentStyle}
          onChange={(e) => changeAgentStyle(e.target.value)}
        >
          <option value="Casual">Casual</option>
          <option value="Energetic">Energetic</option>
          <option value="Formal">Formal</option>
          <option value="Academic">Academic</option>
          <option value="Robot">Robot</option>
        </select>
      </div>

      <button onClick={handleSave}>Save</button>
    </div>
  )
}

export default Account