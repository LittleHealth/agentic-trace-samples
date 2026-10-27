# 软件修复

[首页](../../README.md)

查看文件、复现问题、修改代码和运行测试。共 3 条样本。

| 样本 | 任务 | 来源状态 | 阅读入口 |
|---|---|---|---|
| 1. 修复非 POSIX 路径 | 修复 GetEdk2RelativePathFromAbsolutePath() 对混合路径分隔符的处理。 | submit；resolved=1 | [步骤](01-posix-path/README.md) · [可读 JSON](01-posix-path/trace.json) · [原始 JSON](01-posix-path/trace.raw.json) |
| 2. 修复 NetCDF 变量名中的斜杠 | 处理变量名含斜杠时写入 NetCDF 失败的问题。 | submit；resolved=0 | [步骤](02-netcdf-variable-names/README.md) · [可读 JSON](02-netcdf-variable-names/trace.json) · [原始 JSON](02-netcdf-variable-names/trace.raw.json) |
| 3. 处理 AndroidTV 的 ADB 查询失败 | 处理获取 AndroidTV app_id 时出现 “Failed to write while dumping” 的情况。 | submit；resolved=0 | [步骤](03-androidtv-adb/README.md) · [可读 JSON](03-androidtv-adb/trace.json) · [原始 JSON](03-androidtv-adb/trace.raw.json) |
