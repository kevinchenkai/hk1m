
#!/bin/bash

# 港股量化交易数据处理脚本
# 作者: 
# 版本: 1.1
# 更新时间: $(date +"%Y-%m-%d")

set -euo pipefail  # 严格模式：遇到错误立即退出，使用未定义变量报错，管道错误不被掩盖

# =============================================================================
# 配置区域
# =============================================================================

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 日志配置
LOG_DIR="${PROJECT_ROOT}/logs"
LOG_FILE="${LOG_DIR}/run_$(date +%Y%m%d_%H%M%S).log"

# Python环境配置
PYTHON_CMD="${PYTHON_CMD:-python3}"
VENV_PATH="${VENV_PATH:-}"

# 数据配置
DATA_DIR="${PROJECT_ROOT}/data"
CLEAN_OLD_DATA="${CLEAN_OLD_DATA:-false}"
DAYS_TO_KEEP="${DAYS_TO_KEEP:-7}"

# =============================================================================
# 工具函数
# =============================================================================

# 日志函数
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_success() { log "SUCCESS" "$@"; }

# 错误处理函数
error_exit() {
    log_error "$1"
    exit 1
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error_exit "命令 '$1' 未找到，请安装后重试"
    fi
}

# 检查Python环境
check_python_env() {
    log_info "检查Python环境..."
    
    # 检查Python命令
    check_command "$PYTHON_CMD"
    
    # 激活虚拟环境（如果指定）
    if [[ -n "$VENV_PATH" && -f "$VENV_PATH/bin/activate" ]]; then
        log_info "激活虚拟环境: $VENV_PATH"
        source "$VENV_PATH/bin/activate"
    fi
    
    # 检查Python版本
    local python_version
    python_version=$($PYTHON_CMD --version 2>&1)
    log_info "使用Python版本: $python_version"
    
    # 检查关键依赖包
    local required_packages=("futu" "pandas")
    for package in "${required_packages[@]}"; do
        if ! $PYTHON_CMD -c "import $package" &>/dev/null; then
            error_exit "缺少Python包: $package，请运行 'pip install $package' 安装"
        fi
    done
    
    log_success "Python环境检查完成"
}

# 创建必要目录
setup_directories() {
    log_info "创建必要目录..."
    mkdir -p "$LOG_DIR" "$DATA_DIR"
    log_success "目录创建完成"
}

# 清理旧数据
cleanup_old_data() {
    if [[ "$CLEAN_OLD_DATA" == "true" ]]; then
        log_info "清理 $DAYS_TO_KEEP 天前的旧数据..."
        find "$DATA_DIR" -type f -mtime +$DAYS_TO_KEEP -delete 2>/dev/null || true
        log_success "旧数据清理完成"
    fi
}

# 执行Python脚本
execute_python_script() {
    local script_name="$1"
    local description="$2"
    local script_path="${SCRIPT_DIR}/${script_name}"
    
    if [[ ! -f "$script_path" ]]; then
        error_exit "脚本文件不存在: $script_path"
    fi
    
    log_info "开始执行: $description"
    log_info "脚本路径: $script_path"
    
    # 切换到项目根目录执行，确保相对路径正确
    cd "$PROJECT_ROOT"
    
    if $PYTHON_CMD "$script_path"; then
        log_success "$description 执行成功"
        return 0
    else
        local exit_code=$?
        error_exit "$description 执行失败，退出码: $exit_code"
    fi
}

# 显示脚本帮助
show_help() {
    cat << EOF
港股量化交易数据处理脚本

用法: $0 [选项]

选项:
  -h, --help              显示此帮助信息
  -v, --verbose           显示详细输出
  -c, --clean             执行前清理旧数据
  --python-cmd COMMAND    指定Python命令 (默认: python3)
  --venv-path PATH        虚拟环境路径
  --days-to-keep N        保留数据天数 (默认: 7)

环境变量:
  PYTHON_CMD             Python命令
  VENV_PATH             虚拟环境路径
  CLEAN_OLD_DATA        是否清理旧数据 (true/false)
  DAYS_TO_KEEP          保留数据天数

示例:
  $0                                    # 使用默认配置运行
  $0 --clean                           # 运行前清理旧数据
  $0 --python-cmd python3.9           # 使用指定Python版本
  $0 --venv-path /path/to/venv         # 使用虚拟环境

EOF
}

# =============================================================================
# 主程序
# =============================================================================

main() {
    local start_time=$(date +%s)
    
    log_info "=================================="
    log_info "港股量化交易数据处理开始"
    log_info "=================================="
    log_info "项目根目录: $PROJECT_ROOT"
    log_info "日志文件: $LOG_FILE"
    
    # 前置检查
    setup_directories
    check_python_env
    cleanup_old_data
    
    # 执行主要流程
    log_info "开始执行数据处理流程..."
    
    # 1. 获取K线数据
    execute_python_script "get_klines.py" "获取K线数据"
    
    # 2. 获取订单信息
    execute_python_script "get_order.py" "获取订单信息"
    
    # 3. 构建交易提示语
    execute_python_script "build_prompt.py" "生成交易提示语"
    
    # 计算执行时间
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log_info "=================================="
    log_success "所有任务执行完成！总耗时: ${duration}秒"
    log_info "日志文件: $LOG_FILE"
    log_info "=================================="
}

# =============================================================================
# 参数解析
# =============================================================================

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            set -x  # 开启详细模式
            shift
            ;;
        -c|--clean)
            CLEAN_OLD_DATA="true"
            shift
            ;;
        --python-cmd)
            PYTHON_CMD="$2"
            shift 2
            ;;
        --venv-path)
            VENV_PATH="$2"
            shift 2
            ;;
        --days-to-keep)
            DAYS_TO_KEEP="$2"
            shift 2
            ;;
        *)
            error_exit "未知选项: $1。使用 --help 查看帮助信息"
            ;;
    esac
done

# 捕获中断信号
trap 'log_error "脚本被用户中断"; exit 130' INT TERM

# 执行主程序
main "$@"
