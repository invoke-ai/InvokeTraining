@echo off
setlocal enabledelayedexpansion

:menu
echo.
echo Select a merge method:
echo 1. Merge Models
echo 2. Merge LoRA into Model
echo 3. Merge Task Models to Base Model
echo 4. Extract LoRA from Model Diff
echo 5. Exit
set /p choice="Enter your choice: "

if "%choice%"=="1" goto merge_models
if "%choice%"=="2" goto merge_lora_into_model
if "%choice%"=="3" goto merge_task_models_to_base_model
if "%choice%"=="4" goto extract_lora_from_model_diff
if "%choice%"=="5" goto end

:merge_models
set /p model_type="Enter model type (SD/SDXL): "
set /p models="Enter models (space-separated): "
set /p weights="Enter weights (space-separated): "
set /p method="Enter method (LERP/SLERP): "
set /p out_dir="Enter output directory: "
set /p dtype="Enter dtype (float32/float16/bfloat16): "
python src\invoke_training\model_merge\scripts\merge_models.py --model-type %model_type% --models %models% --weights %weights% --method %method% --out-dir %out_dir% --dtype %dtype%
goto end

:merge_lora_into_model
set /p model_type="Enter model type (SD/SDXL): "
set /p base_model="Enter base model: "
set /p lora_models="Enter LoRA models (space-separated): "
set /p output="Enter output directory: "
set /p save_dtype="Enter save dtype (float32/float16/bfloat16): "
python src\invoke_training\model_merge\scripts\merge_lora_into_model.py --model-type %model_type% --base-model %base_model% --lora-models %lora_models% --output %output% --save-dtype %save_dtype%
goto end

:merge_task_models_to_base_model
set /p model_type="Enter model type (SD/SDXL): "
set /p base_model="Enter base model: "
set /p task_models="Enter task models (space-separated): "
set /p task_weights="Enter task weights (space-separated): "
set /p method="Enter method (TIES/DARE_LINEAR/DARE_TIES): "
set /p density="Enter density (0-1): "
set /p out_dir="Enter output directory: "
set /p dtype="Enter dtype (float32/float16/bfloat16): "
python src\invoke_training\model_merge\scripts\merge_task_models_to_base_model.py --model-type %model_type% --base-model %base_model% --task-models %task_models% --task-weights %task_weights% --method %method% --density %density% --out-dir %out_dir% --dtype %dtype%
goto end

:extract_lora_from_model_diff
set /p model_type="Enter model type (SD/SDXL): "
set /p model_orig="Enter original model: "
set /p model_tuned="Enter tuned model: "
set /p save_to="Enter save to path: "
set /p load_precision="Enter load precision (float32/float16/bfloat16): "
set /p save_precision="Enter save precision (float32/float16/bfloat16): "
set /p lora_rank="Enter LoRA rank: "
set /p clamp_quantile="Enter clamp quantile (0-1): "
set /p device="Enter device (cuda/cpu): "
python src\invoke_training\model_merge\scripts\extract_lora_from_model_diff.py --model-type %model_type% --model-orig %model_orig% --model-tuned %model_tuned% --save-to %save_to% --load-precision %load_precision% --save-precision %save_precision% --lora-rank %lora_rank% --clamp-quantile %clamp_quantile% --device %device%
goto end

:end
echo Exiting...