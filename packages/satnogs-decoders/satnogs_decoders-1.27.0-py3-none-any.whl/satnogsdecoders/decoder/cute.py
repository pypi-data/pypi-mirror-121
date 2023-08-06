# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cute(KaitaiStruct):
    """:field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field rpt_callsign: ax25_frame.ax25_header.repeater.rpt_instance[0].rpt_callsign_raw.callsign_ror.callsign
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field ccsds_version: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.ccsds_version
    :field packet_type: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.packet_type
    :field secondary_header_flag: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.secondary_header_flag
    :field application_process_id: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.application_process_id
    :field sequence_flag: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.sequence_flag
    :field packet_id: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.packet_id
    :field data_length: ax25_frame.payload.ax25_info.ccsds_space_packet.packet_primary_header.data_length
    :field time_stamp_seconds: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.secondary_header.time_stamp_seconds
    :field sub_seconds: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.secondary_header.sub_seconds
    :field soh_l0_wdt_2sec_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_wdt_2sec_cnt
    :field soh_l0_reset_armed: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_reset_armed
    :field soh_l0_wdt_stat: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_wdt_stat
    :field soh_l0_wdt_en: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_wdt_en
    :field soh_l0_table_select: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_table_select
    :field soh_l0_boot_relay: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_boot_relay
    :field soh_l0_l0_acpt_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_l0_acpt_cnt
    :field soh_l0_l0_rjct_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_l0_rjct_cnt
    :field soh_l0_hw_sec_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_hw_sec_cnt
    :field soh_l0_time_tag: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_time_tag
    :field soh_l0_pld_tlm_ack_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_pld_tlm_ack_cnt
    :field soh_l0_pld_cmd_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_pld_cmd_cnt
    :field soh_l0_pld_tlm_to_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_pld_tlm_to_cnt
    :field soh_l0_pld_nak_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_pld_nak_cnt
    :field soh_l0_spare_end_l: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_spare_end_l
    :field soh_l0_spare_end_h: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_l0.soh_l0_spare_end_h
    :field soh_command_tlm_cmd_status: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_cmd_status
    :field soh_command_tlm_realtime_cmd_accept_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_realtime_cmd_accept_cnt
    :field soh_command_tlm_realtime_command_reject_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_realtime_command_reject_cnt
    :field soh_command_tlm_stored_command_accept_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_stored_command_accept_cnt
    :field soh_command_tlm_macros_executoing_pack1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_macros_executoing_pack1
    :field soh_command_tlm_macros_executoing_pack2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_command_tlm.soh_command_tlm_macros_executoing_pack2
    :field soh_general_scrub_status_overall: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_general.soh_general_scrub_status_overall
    :field soh_general_image_booted: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_general.soh_general_image_booted
    :field soh_general_image_auto_failover: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_general.soh_general_image_auto_failover
    :field soh_time_tai_seconds: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_time.soh_time_tai_seconds
    :field soh_time_time_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_time.soh_time_time_valid
    :field soh_refs_position_wrt_eci1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_position_wrt_eci1
    :field soh_refs_position_wrt_eci2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_position_wrt_eci2
    :field soh_refs_position_wrt_eci3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_position_wrt_eci3
    :field soh_refs_velocity_wrt_eci1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_velocity_wrt_eci1
    :field soh_refs_velocity_wrt_eci2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_velocity_wrt_eci2
    :field soh_refs_velocity_wrt_eci3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_velocity_wrt_eci3
    :field soh_refs_refs_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_refs.soh_refs_refs_valid
    :field soh_att_det_q_body_wrt_eci1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_q_body_wrt_eci1
    :field soh_att_det_q_body_wrt_eci2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_q_body_wrt_eci2
    :field soh_att_det_q_body_wrt_eci3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_q_body_wrt_eci3
    :field soh_att_det_q_body_wrt_eci4: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_q_body_wrt_eci4
    :field soh_att_det_body_rate1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_body_rate1
    :field soh_att_det_body_rate2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_body_rate2
    :field soh_att_det_body_rate3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_body_rate3
    :field soh_att_det_bad_att_timer: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_bad_att_timer
    :field soh_att_det_bad_rate_timer: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_bad_rate_timer
    :field soh_att_det_reinit_count: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_reinit_count
    :field soh_att_det_attitude_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_attitude_valid
    :field soh_att_det_meas_att_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_meas_att_valid
    :field soh_att_det_meas_rate_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_meas_rate_valid
    :field soh_att_det_trackder_used: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_det.soh_att_det_trackder_used
    :field soh_att_cmd_hr_cycle_safe_mode: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_cmd.soh_att_cmd_hr_cycle_safe_mode
    :field soh_att_cmd_rotisserie_rate: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_cmd.soh_att_cmd_rotisserie_rate
    :field soh_att_cmd_adcs_mode: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_cmd.soh_att_cmd_adcs_mode
    :field soh_att_cmd_safe_mode_reason: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_cmd.soh_att_cmd_safe_mode_reason
    :field soh_att_cmd_recommend_sun_point: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_cmd.soh_att_cmd_recommend_sun_point
    :field soh_rw_drive_filtered_speed_rpm1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_rw_drive.soh_rw_drive_filtered_speed_rpm1
    :field soh_rw_drive_filtered_speed_rpm2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_rw_drive.soh_rw_drive_filtered_speed_rpm2
    :field soh_rw_drive_filtered_speed_rpm3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_rw_drive.soh_rw_drive_filtered_speed_rpm3
    :field soh_tracker_operating_mode: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker.soh_tracker_operating_mode
    :field soh_tracker_star_id_step: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker.soh_tracker_star_id_step
    :field soh_tracker_att_status: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker.soh_tracker_att_status
    :field soh_tracker_num_attitude_stars: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker.soh_tracker_num_attitude_stars
    :field soh_att_ctrl_position_error1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_position_error1
    :field soh_att_ctrl_position_error2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_position_error2
    :field soh_att_ctrl_position_error3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_position_error3
    :field soh_att_ctrl_time_into_search: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_time_into_search
    :field soh_att_ctrl_wait_timer: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_wait_timer
    :field soh_att_ctrl_sun_point_angle_error: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_sun_point_angle_error
    :field soh_att_ctrl_sun_point_state: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_att_ctrl.soh_att_ctrl_sun_point_state
    :field soh_momentum_momentum_vector_body1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_momentum_vector_body1
    :field soh_momentum_momentum_vector_body2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_momentum_vector_body2
    :field soh_momentum_momentum_vector_body3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_momentum_vector_body3
    :field soh_momentum_duty_cycle1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_duty_cycle1
    :field soh_momentum_duty_cycle2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_duty_cycle2
    :field soh_momentum_duty_cycle3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_duty_cycle3
    :field soh_momentum_torque_rod_mode1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_torque_rod_mode1
    :field soh_momentum_torque_rod_mode2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_torque_rod_mode2
    :field soh_momentum_torque_rod_mode3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_torque_rod_mode3
    :field soh_momentum_mag_source_used: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_mag_source_used
    :field soh_momentum_momentum_vector_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_momentum.soh_momentum_momentum_vector_valid
    :field soh_css_sun_vector_body1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_css.soh_css_sun_vector_body1
    :field soh_css_sun_vector_body2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_css.soh_css_sun_vector_body2
    :field soh_css_sun_vector_body3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_css.soh_css_sun_vector_body3
    :field soh_css_sun_vector_status: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_css.soh_css_sun_vector_status
    :field soh_css_sun_sensor_used: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_css.soh_css_sun_sensor_used
    :field soh_mag_mag_vector_body1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_mag.soh_mag_mag_vector_body1
    :field soh_mag_mag_vector_body2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_mag.soh_mag_mag_vector_body2
    :field soh_mag_mag_vector_body3: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_mag.soh_mag_mag_vector_body3
    :field soh_mag_mag_vector_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_mag.soh_mag_mag_vector_valid
    :field soh_imu_new_packet_count: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_imu.soh_imu_new_packet_count
    :field soh_imu_imu_vector_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_imu.soh_imu_imu_vector_valid
    :field soh_clock_sync_hr_run_count: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_clock_sync.soh_clock_sync_hr_run_count
    :field soh_clock_sync_hr_exec_time_ms: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_clock_sync.soh_clock_sync_hr_exec_time_ms
    :field soh_analogs_box1_temp: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_analogs.soh_analogs_box1_temp
    :field soh_analogs_bus_voltage: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_analogs.soh_analogs_bus_voltage
    :field soh_analogs_battery_voltage: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_analogs.soh_analogs_battery_voltage
    :field soh_analogs_battery_current: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_analogs.soh_analogs_battery_current
    :field soh_tracker2_operating_mode: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker2.soh_tracker2_operating_mode
    :field soh_tracker2_star_id_step: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker2.soh_tracker2_star_id_step
    :field soh_tracker2_att_status: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker2.soh_tracker2_att_status
    :field soh_tracker2_num_attitude_stars: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker2.soh_tracker2_num_attitude_stars
    :field soh_gps_gps_lock_cnt: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_gps.soh_gps_gps_lock_cnt
    :field soh_gps_gps_valid: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_gps.soh_gps_gps_valid
    :field soh_gps_gps_enable: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_gps.soh_gps_gps_enable
    :field soh_event_check_latched_resp_fire_pack1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_event_check.soh_event_check_latched_resp_fire_pack1
    :field soh_event_check_latched_resp_fire_pack2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_event_check.soh_event_check_latched_resp_fire_pack2
    :field soh_radio_sd_minute_cur: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sd_minute_cur
    :field soh_radio_sd_percent_used_total: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sd_percent_used_total
    :field soh_radio_sd_ok: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sd_ok
    :field soh_radio_sd_fault_count: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sd_fault_count
    :field soh_radio_sdr_tx_tx_frames: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sdr_tx_tx_frames
    :field soh_radio_sdr_tx_temp: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sdr_tx_temp
    :field soh_radio_tx_comm_error: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_tx_comm_error
    :field soh_radio_sq_channel: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sq_channel
    :field soh_radio_sq_trap_count: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sq_trap_count
    :field soh_radio_sq_temp: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_radio.soh_radio_sq_temp
    :field soh_tracker_ctrl_aid_status1: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker_ctrl.soh_tracker_ctrl_aid_status1
    :field soh_tracker_ctrl_aid_status2: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker_ctrl.soh_tracker_ctrl_aid_status2
    :field soh_tracker_ctrl_star_id_status: ax25_frame.payload.ax25_info.ccsds_space_packet.data_section.user_data_field.soh_tracker_ctrl.soh_tracker_ctrl_star_id_status
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Cute.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Cute.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = Cute.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = Cute.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = Cute.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = Cute.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = Cute.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = Cute.IFrame(self._io, self, self._root)


    class CuteBctSohT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_l0 = Cute.SohL0T(self._io, self, self._root)
            self.soh_command_tlm = Cute.SohCommandTlmT(self._io, self, self._root)
            self.soh_general = Cute.SohGeneralT(self._io, self, self._root)
            self.soh_time = Cute.SohTimeT(self._io, self, self._root)
            self.soh_refs = Cute.SohRefsT(self._io, self, self._root)
            self.soh_att_det = Cute.SohAttDetT(self._io, self, self._root)
            self.soh_att_cmd = Cute.SohAttCmdT(self._io, self, self._root)
            self.soh_rw_drive = Cute.SohRwDriveT(self._io, self, self._root)
            self.soh_tracker = Cute.SohTrackerT(self._io, self, self._root)
            self.soh_att_ctrl = Cute.SohAttCtrlT(self._io, self, self._root)
            self.soh_momentum = Cute.SohMomentumT(self._io, self, self._root)
            self.soh_css = Cute.SohCssT(self._io, self, self._root)
            self.soh_mag = Cute.SohMagT(self._io, self, self._root)
            self.soh_imu = Cute.SohImuT(self._io, self, self._root)
            self.soh_clock_sync = Cute.SohClockSyncT(self._io, self, self._root)
            self.soh_analogs = Cute.SohAnalogsT(self._io, self, self._root)
            self.soh_tracker2 = Cute.SohTracker2T(self._io, self, self._root)
            self.soh_gps = Cute.SohGpsT(self._io, self, self._root)
            self.soh_event_check = Cute.SohEventCheckT(self._io, self, self._root)
            self.soh_radio = Cute.SohRadioT(self._io, self, self._root)
            self.soh_tracker_ctrl = Cute.SohTrackerCtrlT(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Cute.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Cute.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Cute.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Cute.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = Cute.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Cute.Ax25InfoData(_io__raw_ax25_info, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not  ((self.callsign == u"CUTE  ") or (self.callsign == u"BCT   ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/callsign/seq/0")


    class SohClockSyncT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_clock_sync_hr_run_count = self._io.read_bits_int_be(32)
            self.soh_clock_sync_hr_exec_time_ms = self._io.read_bits_int_be(8)


    class SohAttCmdT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_att_cmd_hr_cycle_safe_mode = self._io.read_bits_int_be(32)
            self.soh_att_cmd_rotisserie_rate = self._io.read_bits_int_be(16)
            self.soh_att_cmd_adcs_mode = self._io.read_bits_int_be(8)
            self.soh_att_cmd_safe_mode_reason = self._io.read_bits_int_be(8)
            self.soh_att_cmd_recommend_sun_point = self._io.read_bits_int_be(8)


    class SohTrackerCtrlT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_tracker_ctrl_aid_status1 = self._io.read_bits_int_be(8)
            self.soh_tracker_ctrl_aid_status2 = self._io.read_bits_int_be(8)
            self.soh_tracker_ctrl_star_id_status = self._io.read_bits_int_be(8)


    class SohTimeT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_time_tai_seconds = self._io.read_bits_int_be(32)
            self.soh_time_time_valid = self._io.read_bits_int_be(8)


    class SohGpsT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_gps_gps_lock_cnt = self._io.read_bits_int_be(16)
            self.soh_gps_gps_valid = self._io.read_bits_int_be(8)
            self.soh_gps_gps_enable = self._io.read_bits_int_be(8)


    class SohRwDriveT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_rw_drive_filtered_speed_rpm1 = self._io.read_bits_int_be(16)
            self.soh_rw_drive_filtered_speed_rpm2 = self._io.read_bits_int_be(16)
            self.soh_rw_drive_filtered_speed_rpm3 = self._io.read_bits_int_be(16)


    class SohAnalogsT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_analogs_box1_temp = self._io.read_bits_int_be(16)
            self.soh_analogs_bus_voltage = self._io.read_bits_int_be(16)
            self.soh_analogs_battery_voltage = self._io.read_bits_int_be(16)
            self.soh_analogs_battery_current = self._io.read_bits_int_be(16)


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Cute.Ax25InfoData(_io__raw_ax25_info, self, self._root)


    class SohRadioT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_radio_sd_minute_cur = self._io.read_bits_int_be(32)
            self.soh_radio_sd_percent_used_total = self._io.read_bits_int_be(8)
            self.soh_radio_sd_ok = self._io.read_bits_int_be(8)
            self.soh_radio_sd_fault_count = self._io.read_bits_int_be(8)
            self.soh_radio_sdr_tx_tx_frames = self._io.read_bits_int_be(32)
            self.soh_radio_sdr_tx_temp = self._io.read_bits_int_be(8)
            self.soh_radio_tx_comm_error = self._io.read_bits_int_be(8)
            self.soh_radio_sq_channel = self._io.read_bits_int_be(8)
            self.soh_radio_sq_trap_count = self._io.read_bits_int_be(8)
            self.soh_radio_sq_temp = self._io.read_bits_int_be(8)


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class SohTrackerT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_tracker_operating_mode = self._io.read_bits_int_be(8)
            self.soh_tracker_star_id_step = self._io.read_bits_int_be(8)
            self.soh_tracker_att_status = self._io.read_bits_int_be(8)
            self.soh_tracker_num_attitude_stars = self._io.read_bits_int_be(8)


    class SohImuT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_imu_new_packet_count = self._io.read_bits_int_be(8)
            self.soh_imu_imu_vector_valid = self._io.read_bits_int_be(8)


    class DataSectionT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            if self._parent.packet_primary_header.secondary_header_flag:
                self._raw_secondary_header = self._io.read_bytes(6)
                _io__raw_secondary_header = KaitaiStream(BytesIO(self._raw_secondary_header))
                self.secondary_header = Cute.SecondaryHeaderT(_io__raw_secondary_header, self, self._root)

            _on = self._parent.packet_primary_header.application_process_id
            if _on == 86:
                self.user_data_field = Cute.CuteBctSohT(self._io, self, self._root)


    class SohMomentumT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_momentum_momentum_vector_body1 = self._io.read_bits_int_be(16)
            self.soh_momentum_momentum_vector_body2 = self._io.read_bits_int_be(16)
            self.soh_momentum_momentum_vector_body3 = self._io.read_bits_int_be(16)
            self.soh_momentum_duty_cycle1 = self._io.read_bits_int_be(8)
            self.soh_momentum_duty_cycle2 = self._io.read_bits_int_be(8)
            self.soh_momentum_duty_cycle3 = self._io.read_bits_int_be(8)
            self.soh_momentum_torque_rod_mode1 = self._io.read_bits_int_be(8)
            self.soh_momentum_torque_rod_mode2 = self._io.read_bits_int_be(8)
            self.soh_momentum_torque_rod_mode3 = self._io.read_bits_int_be(8)
            self.soh_momentum_mag_source_used = self._io.read_bits_int_be(8)
            self.soh_momentum_momentum_vector_valid = self._io.read_bits_int_be(8)


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = Cute.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = Cute.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = Cute.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class CuteBctFswT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bct_fsw_data = self._io.read_bytes_full()


    class SohCssT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_css_sun_vector_body1 = self._io.read_bits_int_be(16)
            self.soh_css_sun_vector_body2 = self._io.read_bits_int_be(16)
            self.soh_css_sun_vector_body3 = self._io.read_bits_int_be(16)
            self.soh_css_sun_vector_status = self._io.read_bits_int_be(8)
            self.soh_css_sun_sensor_used = self._io.read_bits_int_be(8)


    class SecondaryHeaderT(KaitaiStruct):
        """The Secondary Header is a feature of the Space Packet which allows
        additional types of information that may be useful to the user
        application (e.g., a time code) to be included.
        See: 4.1.3.2 in CCSDS 133.0-B-1
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.time_stamp_seconds = self._io.read_bits_int_be(32)
            self.sub_seconds = self._io.read_bits_int_be(8)
            self.pad = self._io.read_bits_int_be(1) != 0


    class SohEventCheckT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_event_check_latched_resp_fire_pack1 = self._io.read_bits_int_be(8)
            self.soh_event_check_latched_resp_fire_pack2 = self._io.read_bits_int_be(8)


    class SohTracker2T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_tracker2_operating_mode = self._io.read_bits_int_be(8)
            self.soh_tracker2_star_id_step = self._io.read_bits_int_be(8)
            self.soh_tracker2_att_status = self._io.read_bits_int_be(8)
            self.soh_tracker2_num_attitude_stars = self._io.read_bits_int_be(8)


    class SohMagT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_mag_mag_vector_body1 = self._io.read_bits_int_be(16)
            self.soh_mag_mag_vector_body2 = self._io.read_bits_int_be(16)
            self.soh_mag_mag_vector_body3 = self._io.read_bits_int_be(16)
            self.soh_mag_mag_vector_valid = self._io.read_bits_int_be(8)


    class PacketPrimaryHeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ccsds_version = self._io.read_bits_int_be(3)
            self.packet_type = self._io.read_bits_int_be(1) != 0
            self.secondary_header_flag = self._io.read_bits_int_be(1) != 0
            self.application_process_id = self._io.read_bits_int_be(11)
            self.sequence_flag = self._io.read_bits_int_be(2)
            self.packet_id = self._io.read_bits_int_be(14)
            self.data_length = self._io.read_bits_int_be(16)


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = Cute.Callsign(_io__raw_callsign_ror, self, self._root)


    class SohGeneralT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_general_scrub_status_overall = self._io.read_bits_int_be(8)
            self.soh_general_image_booted = self._io.read_bits_int_be(8)
            self.soh_general_image_auto_failover = self._io.read_bits_int_be(8)


    class SohAttCtrlT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_att_ctrl_position_error1 = self._io.read_bits_int_be(32)
            self.soh_att_ctrl_position_error2 = self._io.read_bits_int_be(32)
            self.soh_att_ctrl_position_error3 = self._io.read_bits_int_be(32)
            self.soh_att_ctrl_time_into_search = self._io.read_bits_int_be(16)
            self.soh_att_ctrl_wait_timer = self._io.read_bits_int_be(16)
            self.soh_att_ctrl_sun_point_angle_error = self._io.read_bits_int_be(16)
            self.soh_att_ctrl_sun_point_state = self._io.read_bits_int_be(8)


    class CcsdsSpacePacketT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_packet_primary_header = self._io.read_bytes(6)
            _io__raw_packet_primary_header = KaitaiStream(BytesIO(self._raw_packet_primary_header))
            self.packet_primary_header = Cute.PacketPrimaryHeaderT(_io__raw_packet_primary_header, self, self._root)
            self.data_section = Cute.DataSectionT(self._io, self, self._root)


    class SohL0T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_l0_wdt_2sec_cnt = self._io.read_bits_int_be(3)
            self.soh_l0_reset_armed = self._io.read_bits_int_be(1) != 0
            self.soh_l0_wdt_stat = self._io.read_bits_int_be(1) != 0
            self.soh_l0_wdt_en = self._io.read_bits_int_be(1) != 0
            self.soh_l0_table_select = self._io.read_bits_int_be(1) != 0
            self.soh_l0_boot_relay = self._io.read_bits_int_be(1) != 0
            self.soh_l0_l0_acpt_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_l0_rjct_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_hw_sec_cnt = self._io.read_bits_int_be(8)
            self.pad0 = self._io.read_bits_int_be(32)
            self.pad0_1 = self._io.read_bits_int_be(32)
            self.soh_l0_time_tag = self._io.read_bits_int_be(32)
            self.pad1 = self._io.read_bits_int_be(32)
            self.soh_l0_pld_tlm_ack_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_pld_cmd_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_pld_tlm_to_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_pld_nak_cnt = self._io.read_bits_int_be(8)
            self.soh_l0_spare_end_l = self._io.read_bits_int_be(32)
            self.soh_l0_spare_end_h = self._io.read_bits_int_be(32)


    class SohRefsT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_refs_position_wrt_eci1 = self._io.read_bits_int_be(32)
            self.soh_refs_position_wrt_eci2 = self._io.read_bits_int_be(32)
            self.soh_refs_position_wrt_eci3 = self._io.read_bits_int_be(32)
            self.soh_refs_velocity_wrt_eci1 = self._io.read_bits_int_be(32)
            self.soh_refs_velocity_wrt_eci2 = self._io.read_bits_int_be(32)
            self.soh_refs_velocity_wrt_eci3 = self._io.read_bits_int_be(32)
            self.soh_refs_refs_valid = self._io.read_bits_int_be(8)


    class SohAttDetT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_att_det_q_body_wrt_eci1 = self._io.read_bits_int_be(32)
            self.soh_att_det_q_body_wrt_eci2 = self._io.read_bits_int_be(32)
            self.soh_att_det_q_body_wrt_eci3 = self._io.read_bits_int_be(32)
            self.soh_att_det_q_body_wrt_eci4 = self._io.read_bits_int_be(32)
            self.soh_att_det_body_rate1 = self._io.read_bits_int_be(32)
            self.soh_att_det_body_rate2 = self._io.read_bits_int_be(32)
            self.soh_att_det_body_rate3 = self._io.read_bits_int_be(32)
            self.soh_att_det_bad_att_timer = self._io.read_bits_int_be(32)
            self.soh_att_det_bad_rate_timer = self._io.read_bits_int_be(32)
            self.soh_att_det_reinit_count = self._io.read_bits_int_be(32)
            self.soh_att_det_attitude_valid = self._io.read_bits_int_be(8)
            self.soh_att_det_meas_att_valid = self._io.read_bits_int_be(8)
            self.soh_att_det_meas_rate_valid = self._io.read_bits_int_be(8)
            self.soh_att_det_trackder_used = self._io.read_bits_int_be(8)


    class SohCommandTlmT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.soh_command_tlm_cmd_status = self._io.read_bits_int_be(8)
            self.soh_command_tlm_realtime_cmd_accept_cnt = self._io.read_bits_int_be(8)
            self.soh_command_tlm_realtime_command_reject_cnt = self._io.read_bits_int_be(8)
            self.soh_command_tlm_stored_command_accept_cnt = self._io.read_bits_int_be(8)
            self.soh_command_tlm_macros_executoing_pack1 = self._io.read_bits_int_be(8)
            self.soh_command_tlm_macros_executoing_pack2 = self._io.read_bits_int_be(8)


    class Ax25InfoData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ccsds_space_packet = Cute.CcsdsSpacePacketT(self._io, self, self._root)



