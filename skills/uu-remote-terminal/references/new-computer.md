# 新电脑怎么配置与测试

本文件给后续 agent 指路，不需要重新设计一套工具。参考本机已安装的 `uu-remote-terminal` 运行时项目，使用前确认实际路径；运行时代码不随此 skill 分发。当前实现支持 macOS 主控端和 Windows PowerShell 7 被控端；其他系统需要另外适配。

## 接入思路

1. **确认目标。** 用 UU 的设备列表核对用户指定电脑的 deviceId、在线状态和系统。不要默认选第一台；UU 显示名不一定等于 Windows 主机名。
2. **确认 PowerShell 7。** 在远端运行 `pwsh --version`。Microsoft Store 版可能通过 WindowsApps 别名启动，不要只认 `C:\Program Files\PowerShell\7\pwsh.exe`。
3. **独立配置。** 在运行时 `config/targets.json` 增加独立目标，例如 `office`，记录已核验的 `deviceId`、`displayNames`、`port`、`capability`、`keyEnv`、`computer`、`user`。新电脑分配独立 Keychain 能力、公钥和本地端口，例如 `uu-remote-office`、`UU_REMOTE_OFFICE_PRIVATE_KEY`、`37892`。入口已支持 `--target office`，无需复制客户端代码。不要覆盖旧目标的公钥、配置或映射，也不要复用它的密钥。
4. **生成密钥。** 参考运行时项目中的 `scripts/provision-key.mjs` 和 `scripts/keychain-store.swift`，私钥直接存本机 Keychain，远端只放公钥。这些生成和部署脚本仍是旧目标专用，不会自动读取 targets.json。先在隔离的暂存目录适配能力名、变量名、公钥路径和部署输出，核对后再运行；不能直接在旧目标目录重新生成。
5. **首次启动。** 参考已为新目标适配的 `scripts/deploy.mjs --prepare` 生成包含程序与公钥的启动命令，通过已认证的目标 UU 终端执行一次。没有可靠的程序化首次输入路径时，请用户粘贴一次即可；不自动调用 GUI 脚本或打开远控窗口。
6. **设置映射。** 在本机 UU 的目标设备中，将新的本地端口（如 `37892`）映射到该机 `127.0.0.1:37891`。本地也应只监听回环地址。不同电脑的本地端口必须不同，远端各用自己的 `37891` 即可。

远端默认安装目录是 `%LOCALAPPDATA%\UU-Codex-Bridge`。如果已经存在其他有效桥接，先查归属，不覆盖公钥。当前 Mac UU 的 `term` 只打开终端列表、`lterm` 管理本机会话，不要假定它们能直接执行远程命令；以已安装版本的 `--help` 为准。

## 怎么算配置成功

通过 `uu-remote --target office` 验证，不能只更改端口复用旧目标凭据。身份预期值必须由已认证的目标会话确认，不通过接受未知 ping 返回值建立信任：

- `ping` 返回正确主机、用户和 PowerShell 7 版本。
- 执行 `hostname`、`whoami`，验证中文输出、stderr 和非零退出码。
- 在远端临时目录创建一个测试文件，读回核对后删除。
- 验证超时后能继续调用；有需要时复用 `tests/remote.integration.mjs`，先改好目标身份、能力和端口。
- 关闭 UU 终端界面连接，保留映射，再执行一次命令，确认不依赖图形窗口。

仅看到“映射成功”或“进程已启动”不算验收通过。完成后记录新电脑的 deviceId、主机名、入口路径、端口和能力名，供下一次 agent 使用；不记录私钥。现有其他目标配置保持不变。

## 重启与常见问题

默认桥没有开机自启动。远端重启后，通过 UU 终端重新运行已安装的 `bridge.ps1`，使用 `pwsh` 启动；无需重新生成密钥。完整短命令见运行时目录的 `README.md`。用户没有要求时，不额外安装计划任务或自启动。

连接被拒绝先查本地映射；连接关闭先查远端桥和启动日志；签名失败核对该目标的能力与公钥。`>>` 表示 PowerShell 仍在等待续行，不能认为命令已经执行。若写操作遇到断线，恢复后先核对实际状态，避免重复执行。
