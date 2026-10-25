TEST_PATH="./tests/api_test/soap_api/comparison_testing/${Batches}/steps_def"
docker run --rm \
  --ipc=host \
  --network=host \
  -v "${PWD}:/app" \
  -e "PFX_CERT_PATH=certs/kv-int-dev-aue-001-cloudapi-dev-ssi-govt-nz-20260408.pfx" \
  -e "ENVIRONMENT=${Environment}" \
  -e BUILD_NUMBER \
  -e JOB_NAME \
  -e GIT_BRANCH \
  -e BRANCH_NAME \
  -e GIT_COMMIT \
  integration-tests:latest \
  bash -c "
   pytest "${TEST_PATH}" -n auto \
   $( [ "${Rerun_Failures}" = "true" ] && echo "--lf" ) &&
   python -m tools.test_result_coverage.generator
  "
rm -rf report.json
