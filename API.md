# Debate AI Platform API 文档

## 基础信息
- 基础URL: `http://localhost:8000`
- 所有请求和响应均使用 JSON 格式
- 所有时间戳使用 ISO 8601 格式
- 所有请求的 Content-Type 应设置为 `application/json`（除非特别说明）

## 1. Tutorial API

### 1.1 获取教程问题
**请求方法：** `GET`  
**路径：** `/tutorial/next-question`

**响应示例：**
```json
{
    "example": ["emily happy", "4", "have desert"],
    "question": ["emily has desert", "4", "emily happy"]
}
```

**响应说明：**
- `example`: 示例逻辑表达式的标记列表
- `question`: 需要分析的问题表达式的标记列表

### 1.2 提交答案
**请求方法：** `POST`  
**路径：** `/tutorial/answer`  
**Content-Type:** `application/json`

**请求体：**
```json
{
    "question_id": 1,
    "user_answer": false
}
```

**请求参数说明：**
- `question_id`: 问题的唯一标识符（整数）
- `user_answer`: 用户的答案（布尔值），表示两个逻辑表达式是否等价

**响应示例（正确答案）：**
```json
{
    "correct": true
}
```

**响应示例（错误答案）：**
```json
{
    "correct": false,
    "explanation": "The example and question have different logical structures: 'emily happy' vs 'emily has desert'."
}
```

**错误响应：**
```json
{
    "detail": "Invalid question ID"
}
```

**响应说明：**
- `correct`: 布尔值，表示答案是否正确
- `explanation`: 当答案错误时提供的解释（字符串）
- 如果问题 ID 无效，将返回 400 状态码

## 2. Agent Training API

### 2.1 开始训练会话
**请求方法：** `POST`  
**路径：** `/agent-training/start`

**请求体：**
```json
{
    "topic_id": "climate_change",
    "user_side": "supporting"  // 可选值: "supporting" 或 "opposing"
}
```

**响应示例：**
```json
{
    "conversation_id": "6bb99a33-0674-41a2-8deb-d6e756bfc759",
    "topic": {
        "id": "climate_change",
        "title": "Climate Change",
        "description": "Global warming and climate change: causes, impacts, and solutions"
    },
    "user_side": "supporting"
}
```

### 2.2 提交文本回合
**请求方法：** `POST`  
**路径：** `/agent-training/round/{conversation_id}`

**请求体：**
```json
{
    "user_utterance": "Climate change is real because global temperatures have been rising consistently over the past century."
}
```

**响应示例：**
```json
{
    "user_response": {
        "text": "用户的输入文本",
        "logic_chain": {
            "logic_expression": "逻辑表达式",
            "converted_logical_expression": ["token1", "4", "token2"],
            "performance": {
                "valid": false,
                "valid_explanation": "无效原因的解释",
                "sound": false,
                "sound_explanation": "不合理原因的解释"
            }
        }
    },
    "ai_response": {
        "text": "AI的回应文本",
        "audio_url": "audio_storage/response.mp3",
        "logic_chain": {
            "logic_expression": "AI的逻辑表达式",
            "converted_logical_expression": ["token1", "1", "token2"],
            "performance": {
                "valid": true,
                "valid_explanation": "",
                "sound": false,
                "sound_explanation": "不合理原因的解释"
            }
        }
    },
    "round_id": "e5fe2794-0284-4c4f-b560-a046ea59fee5"
}
```

### 2.3 提交音频回合
**请求方法：** `POST`  
**路径：** `/agent-training/audio/{conversation_id}`  
**Content-Type:** `multipart/form-data`

**请求参数：**
- `file`: WAV 格式音频文件（22050Hz 采样率）
- `speaker_id`: 说话者ID

**响应格式：** 与文本回合相同

### 2.4 获取训练历史
**请求方法：** `GET`  
**路径：** `/agent-training/history/{conversation_id}`

**响应示例：**
```json
{
    "conversation_id": "6bb99a33-0674-41a2-8deb-d6e756bfc759",
    "topic_id": "climate_change",
    "rounds": [
        {
            "round_index": 0,
            "user": {
                "text": "用户的输入",
                "logic_chain": {
                    // 逻辑链详情（格式同上）
                }
            },
            "ai": {
                "text": "AI的回应",
                "audio_url": "音频URL",
                "logic_chain": {
                    // 逻辑链详情（格式同上）
                }
            }
        }
    ]
}
```

### 2.5 获取逻辑链分析
**请求方法：** `GET`  
**路径：** `/agent-training/logic-chain/{conversation_id}`

**响应示例：**
```json
{
    "topic": {
        "id": "climate_change",
        "title": "Climate Change",
        "description": "描述文本"
    },
    "logic_chains": [
        {
            "round_index": 0,
            "user_chain": {
                "text": "用户文本",
                "logic_expression": "逻辑表达式",
                "converted_logical_expression": ["token1", "4", "token2"],
                "performance": {
                    "valid": false,
                    "valid_explanation": "解释",
                    "sound": false,
                    "sound_explanation": "解释"
                }
            },
            "ai_chain": {
                // AI 的逻辑链（格式同上）
            },
            "timestamp": "2024-02-23T19:57:05.845994"
        }
    ]
}
```

### 2.6 获取当前逻辑链
**请求方法：** `GET`  
**路径：** `/agent-training/logic-chain/{conversation_id}/current`

**响应示例：**
```json
{
    "topic": {
        "id": "climate_change",
        "title": "Climate Change",
        "description": "描述文本"
    },
    "current_chain": {
        "round_index": 0,
        "user_chain": {
            // 用户的逻辑链（格式同上）
        },
        "ai_chain": {
            // AI 的逻辑链（格式同上）
        },
        "timestamp": "2024-02-23T19:57:05.845994"
    }
}
```

## 错误处理

所有 API 在发生错误时会返回适当的 HTTP 状态码和错误信息：

```json
{
    "detail": "错误描述信息"
}
```

常见状态码：
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

## 注意事项

### 1. 音频文件要求
- 格式：WAV
- 采样率：22050Hz
- 声道：单声道
- 编码：PCM 16-bit

### 2. 会话管理
- 每个训练会话都有唯一的 `conversation_id`
- 会话状态会在服务器端保持
- 建议定期调用历史记录 API 同步状态

### 3. 逻辑分析
- `logic_expression`: 原始逻辑表达式
- `converted_logical_expression`: 标记化的逻辑表达式
- `performance`: 包含有效性和合理性的分析

### 4. 音频响应
- AI 的回应会同时包含文本和音频
- 音频 URL 可以直接用于播放 